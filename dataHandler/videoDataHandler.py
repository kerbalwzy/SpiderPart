# -*- coding:utf-8 -*-
# python version= python3.X
# code lines count about 100
import re
import time
import requests
from lxml import etree
from threading import Thread
from customTools.loggerHome import videologger
from customTools.queueHome import videoDataQueue
from customTools.fingerPrintHome import data_fingerprint
from customTools.databaseHome import video_redis_client, video_mongo_clinet


def _html_hander(html):
    """
    translate the html text into a new format we need
    :param html:
    :return: new html text
    """
    new_html = re.sub(r'\\"', '"', html)
    new_html = re.sub(r'\\n', "", new_html)
    new_html = re.sub(r'\\', '', new_html)
    # decode the html for twice because the video sources had been encode for twice
    new_html = requests.utils.unquote(new_html)
    new_html = requests.utils.unquote(new_html)
    return new_html


def _get_element(new_html):
    """
    through regex get the target string part list, and create elements for Xpath
    :param new_html:
    :return: elements list
    """
    target_strs = re.findall(r'<div class="WB_detail">.*?<!-- feed区 大数据tag -->                    </div>', new_html)
    elements = [etree.HTML(item) for item in target_strs]
    return elements


def _get_data(elements):
    """
    through Xpath get information strings and composite a dictionary
    :param elements:
    :add the information dictionary into video data queue
    """
    for element in elements:
        video_dict = dict()
        video_dict["intro"] = element.xpath('.//div[@class="WB_text W_f14"]/text()')[0].strip()
        video_dict["video"] = \
            element.xpath('.//li[@class="WB_video  S_bg1 WB_video_mini"]/@video-sources')[0].split(",")[0][8:]
        video_dict["image"] = "http:" + element.xpath('.//div[@node-type="fl_h5_video_pre"]/img/@src')[0]
        videoDataQueue.put(video_dict)


def _check_finger_and_save_data():
    """
    get video information dictionary from video data queue,and then check if it is already saved
    if not, save it into mongodb.
    """
    while True:
        video_dict = videoDataQueue.get()
        # according to video source http root (with out query) to create finger
        video_rote = video_dict["video"].split("?")[0]
        data_finger = data_fingerprint(video_rote)
        result = video_redis_client.sadd("video_data_finger", data_finger)
        if result == 0:
            videologger.info("data repeat which finger with {}".format(data_finger))
        if result == 1:
            video_dict["finger"] = data_finger
            video_dict["addtime"] = time.time()
            video_mongo_clinet.insert_one(video_dict)
            videologger.info("save data :{}".format(video_dict))
        videoDataQueue.task_done()


def data_hander_and_save(html):
    # deal the html string to right format we need
    new_html = _html_hander(html)
    videologger.info("hand the html text into we need successful")
    # get the elements for get data through Xpath
    elements = _get_element(new_html)
    videologger.info("get elements for xpath successful")
    # get data dict
    _get_data(elements)
    # start three threading to check data if already saved and saved the new data
    thread_list = []
    for i in range(3):
        T = Thread(target=_check_finger_and_save_data)
        # set threading name
        T.setName("videoDataHander{}".format(i))
        thread_list.append(T)
    for t in thread_list:
        # set threading follow the main threading
        # than start the threading
        t.setDaemon(True)
        t.start()
        videologger.info("threading which named {} to check and save data".format(T.getName()))
    # join the queue to ensure the main threading won't stop until the queue is empty
    videoDataQueue.join()
    if videoDataQueue.empty():
        videologger.info("video data queus is empty, the spiders will be stop")

