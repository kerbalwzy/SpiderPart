# -*- coding:utf-8 -*-
# python version= python3.X
# code lines count about 100

from threading import Thread
from copy import deepcopy
from customTools.loggerHome import novellogger
from customTools.fingerPrintHome import data_fingerprint
from customTools.respDownloader import get_element
from customTools.disguiser import user_agent
from customTools.queueHome import qiDianNovelElementQueue, qiDianNovelDataQueue
from customTools.databaseHome import novel_redis_client, novel_mongo_clinet


def _get_data():
    """
    through element get data we need ,by xpath
    :param element:
    :return: data dictionary
    """
    while True:
        page_element = qiDianNovelElementQueue.get()

        detail_lis = page_element.xpath('.//div[@id="rank-view-list"]//ul//li')

        for li in detail_lis:
            info_dict = dict()
            image = li.xpath('.//div[@class="book-img-box"]//img/@src')
            name = li.xpath('.//a[@data-eid="qd_C40"]/text()')
            link = li.xpath('.//a[@data-eid="qd_C40"]/@href')
            author = li.xpath('.//a[@class="name"]/text()')
            state = li.xpath('.//p[@class="author"]//span/text()')
            recommend = li.xpath('.//div[@class="total"]//span/text()')

            info_dict["image"] = "http:" + image[0] if len(image) > 0 else None
            info_dict["name"] = str(name[0]) if len(name) > 0 else None
            info_dict["link"] = "https:" + link[0] if len(link) > 0 else None
            info_dict["author"] = str(author[0]) if len(author) > 0 else None
            info_dict["state"] = str(state[0]) if len(state) > 0 else None
            info_dict["recommend"] = int(recommend[0]) if len(recommend) > 0 else None

            if info_dict["link"] and info_dict["name"] is not None:
                qiDianNovelDataQueue.put(deepcopy(info_dict))

        qiDianNovelElementQueue.task_done()

        # print("element queue size:", qiDianNovelElementQueue.qsize())


def _check_and_save():
    """
    get data from novelDataQueue and check this data dictionary if saved by finger print in redis database,
    if not save it
    """
    while True:
        data_dict = qiDianNovelDataQueue.get()

        data_finger = data_fingerprint(data_dict["name"], data_dict["author"], data_dict["link"])

        result = novel_redis_client.sadd("novel_data_finger", data_finger)

        if result == 0:
            novellogger.info("data repeat which finger with :{}".format(data_finger))

        if result == 1:

            headers = {"User-Agent": user_agent(),"Connection":"close"}
            detail_element = get_element(targetUrl=data_dict["link"], workLogger=novellogger, headers=headers)

            wordCount = detail_element.xpath('.//div[@class="book-info "]//p[3]/em[1]/text()')
            intro = detail_element.xpath('//div[@class="book-content-wrap cf"]//div[@class="book-intro"]//text()')
            link = detail_element.xpath('//a[@class="red-btn J-getJumpUrl "]/@href')

            data_dict["source"] = "起点中文网"
            data_dict["wordCount"] = float(wordCount[0]) if len(wordCount) > 0 else None
            data_dict["link"] = "https:" + link[0] if len(link) > 0 else None
            data_dict["intro"] = "".join(intro).strip() if len(intro) > 0 else None
            novel_mongo_clinet.insert_one(data_dict)
            novellogger.info("save data :{}".format(data_dict))

        qiDianNovelDataQueue.task_done()
        # print("data queue size:", qiDianNovelDataQueue.qsize())


def qiDian_data_handler():
    """
    get data from elements and check it and save it
    """
    t1 = Thread(target=_get_data)
    t1.setDaemon(True)
    t1.setName("novelDataHandler1")
    t1.start()
    novellogger.info("threading which named {} begin to hand novel data".format(t1.getName()))

    for i in range(2, 7):
        t2 = Thread(target=_check_and_save)
        t2.setDaemon(True)
        t2.setName("novelDataHandler{}".format(i))
        t2.start()
        novellogger.info("threading which named {} begin to hand novel data".format(t2.getName()))
