# -*- coding:utf-8 -*-
# python version= python3.X
# code lines count about 70

from threading import Thread
from copy import deepcopy
from customTools.loggerHome import novellogger
from customTools.fingerPrintHome import data_fingerprint

from customTools.queueHome import chuangShiELementQueue, chuangShiDataQueue
from customTools.databaseHome import novel_redis_client, novel_mongo_clinet

def _get_data():
    # get data from the page elements by xpath
    while True:
        page_element = chuangShiELementQueue.get()
        name = page_element.xpath('//div[@class="main2"]//div[@class="title"]/strong/a/text()')
        link = page_element.xpath('//div[@class="main2"]//div[@class="title"]/strong/a/@href')
        image = page_element.xpath('//div[@class="main2"]//div[@class="cover"]//img/@src')
        intro = page_element.xpath('//div[@class="main2"]//div[@class="info"]//p/text()')
        author = page_element.xpath('//div[@class="main2"]//div[@class="au_name"]//a/text()')
        wordCount = page_element.xpath('//div[@class="main2"]//div[@class="num"]//td[last()]/text()')
        state = page_element.xpath('//div[@id="novelInfo"]//tr[last()]//span[@class="red2"]/text()')
        recommend = page_element.xpath('//div[@id="novelInfo"]//tr[3]//td[3]/text()')

        info_dict = dict()
        info_dict["image"] = str(image[0]) if len(image) > 0 else None
        info_dict["name"] = str(name[0]) if len(name) > 0 else None
        info_dict["link"] = str(link[0]) if len(name) > 0 else None
        info_dict["intro"] = "".join(intro) if len(intro) > 0 else None
        info_dict["author"] = str(author[0]) if len(author) > 0 else None
        info_dict["state"] = str(state[0][:-1]) if len(state) > 0 else None
        info_dict["wordCount"] = round(float(wordCount[0].split("：")[1]) / 10000, 2) if len(wordCount) > 0 else None
        info_dict["recommend"] = int(recommend[0].split("：")[1]) if len(recommend) > 0 else None

        if info_dict["link"] and info_dict["name"] is not None:
            chuangShiDataQueue.put(deepcopy(info_dict))
        chuangShiELementQueue.task_done()

def _check_and_save():
    """
    get data from novelDataQueue and check this data dictionary if saved by finger print in redis database,
    if not save it
    """
    while True:
        data_dict = chuangShiDataQueue.get()
        data_finger = data_fingerprint(data_dict["name"], data_dict["author"], data_dict["link"])
        result = novel_redis_client.sadd("novel_data_finger", data_finger)

        if result == 0:
            novellogger.info("data repeat which finger with :{}".format(data_finger))
        if result == 1:
            data_dict["source"] = "创世中文网"
            novel_mongo_clinet.insert_one(data_dict)
            novellogger.info("save data :{}".format(data_dict))

        chuangShiDataQueue.task_done()


def chuangShi_data_handler():
    """
    get data from elements and check it and save it
    """
    t1 = Thread(target=_get_data)
    t1.setDaemon(True)
    t1.setName("novelDataHandler2-1")
    t1.start()
    novellogger.info("threading which named {} begin to hand novel data".format(t1.getName()))


    t2 = Thread(target=_check_and_save)
    t2.setDaemon(True)
    t2.setName("novelDataHandler2-2")
    t2.start()
    novellogger.info("threading which named {} begin to hand novel data".format(t2.getName()))

