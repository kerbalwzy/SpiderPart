# -*- coding:utf-8 -*-
# python version= python3.X
# code lines count about 100

import requests
import os
from lxml import etree
from retrying import retry
from threading import Thread
from customTools.disguiser import user_agent
from customTools.loggerHome import musiclogger
from customTools.fingerPrintHome import url_fingerprint
from dataHandler.musicDataHandler import music_data_handler
from customTools.databaseHome import music_redis_client
from customTools.queueHome import musicElemQueus, musicUrlQueue, musicDataQueue


class CloudMusicSpider(object):
    def __init__(self):
        self.start_url = "http://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset={}"
        self.headers = {"User-Agent": user_agent()}
        self.session = requests.session()

    @retry(stop_max_attempt_number=3)
    def _parse_url(self, target_url):
        try:
            response = self.session.get(url=target_url, headers=self.headers, timeout=5)
        except Exception as e:
            musiclogger.error(e)
            raise e
        else:
            musiclogger.info("parse url {} and get response successful!, ".format(target_url))
            return response

    def _get_element(self, url):
        """
        get the element of current html text get from the url
        :param url:
        :return: element
        """
        response = self._parse_url(target_url=url)
        element = etree.HTML(response.text)
        return element

    def get_url_lsit(self, url):
        """
        parse the first url to get the target url list and put the first page element into musicElemQueue.
        :return: target url list
        """
        element = self._get_element(url=url)
        musicElemQueus.put(element)
        try:
            last_page_number = int(element.xpath('//div[@class="u-page"]//a[last()-1]/text()')[0])
            target_urls = [self.start_url.format(i * 35) for i in range(1, last_page_number)]
        except Exception as e:
            musiclogger.info(e)
        else:
            musiclogger.info("get target url list by start url successful")
            return target_urls

    def check_url(self, url):
        """
        check the url if had requested,
        :param url:
        :return: true or false
        """
        url_finger = url_fingerprint(url=url)
        result = music_redis_client.sadd("music_url_finger", url_finger)
        return True if result == 1 else False

    def parse_target_urls(self):
        """
        get target url from musicUrlQueue,
        check the url if requested, if not ,request and get an element put into musicElemQueue
        any way remove this url from musicUrlQueue
        :return:
        """
        while True:
            url = musicUrlQueue.get()
            if self.check_url(url):
                element = self._get_element(url=url)
                musicElemQueus.put(element)
            musicUrlQueue.task_done()

    def run(self):

        target_urls = self.get_url_lsit(self.start_url.format(0))
        for url in target_urls:
            musicUrlQueue.put(url)

        # set threading and start to parse url
        for i in range(8):
            t = Thread(target=self.parse_target_urls)
            t.setDaemon(True)
            t.setName("musicUrlParser{}".format(i))
            t.start()
            musiclogger.info("threading which named {} begin to parse music url".format(t.getName()))

        # start data handlers
        music_data_handler()

        # make all queue join in the main threading, ensure when the all queue is empty the main threading and son \
        # threading will be close and this spiders stop
        for q in [musicUrlQueue, musicElemQueus, musicDataQueue]:
            q.join()


if __name__ == '__main__':
    musicSpider = CloudMusicSpider()
    musicSpider.run()
