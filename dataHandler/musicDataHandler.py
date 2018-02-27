# -*- coding:utf-8 -*-
# python version= python3.X
# code lines count about 70

from threading import Thread
from customTools.loggerHome import musiclogger
from customTools.fingerPrintHome import data_fingerprint
from customTools.queueHome import musicElemQueus, musicDataQueue
from customTools.databaseHome import music_redis_client, music_mongo_clinet


def _get_data():
    """
    through element get data we need ,by xpath
    :param element:
    :return: data dictionary
    """
    while True:
        page_element = musicElemQueus.get()
        detail_divs = page_element.xpath('.//ul[@id="m-pl-container"]//div[@class="u-cover u-cover-1"]')
        for div in detail_divs:
            info_dict = dict()
            image = div.xpath('./img/@src')
            title = div.xpath('./a[@class="msk"]/@title')
            music = div.xpath('./a[@class="msk"]/@href')
            played = div.xpath('.//span[@class="nb"]/text()')
            info_dict["image"] = image[0] if len(image) > 0 else None
            info_dict["title"] = title[0] if len(title) > 0 else None
            info_dict["music"] = "http://music.163.com" + music[0] if len(title) > 0 else None
            if len(played) > 0:
                if "万" in played[0]:
                    info_dict["played"] = int(played[0][0:-1]) * 10000
                else:
                    info_dict["played"] = int(played[0])
            else:
                info_dict["played"] = None
            musicDataQueue.put(info_dict)
        musicElemQueus.task_done()


def _check_and_save():
    """
    get data from musicDataQueue and check this data dictionary if saved by finger print in redis database,
    if not save it
    """
    while True:
        data_dict = musicDataQueue.get()
        data_finger = data_fingerprint(str(data_dict["music"]), str(data_dict["title"]))
        result = music_redis_client.sadd("music_data_finger", data_finger)
        if result == 0:
            musiclogger.info("data repeat which finger with {}".format(data_finger))
        if result == 1:
            music_mongo_clinet.insert_one(data_dict)
            musiclogger.info("save data :{}".format(data_dict))
        musicDataQueue.task_done()


def music_data_handler():
    """
    get data from elements and check it and save it
    """
    t1 = Thread(target=_get_data)
    t1.setDaemon(True)
    t1.setName("musicDataHandler1")
    t1.start()
    musiclogger.info("threading which named {} begin to hand music data".format(t1.getName()))

    t2 = Thread(target=_check_and_save)
    t2.setDaemon(True)
    t2.setName("musicDataHandler2")
    t2.start()
    musiclogger.info("threading which named {} begin to hand music data".format(t2.getName()))


