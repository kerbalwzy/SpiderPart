# -*- coding:utf-8 -*-
# python version= python3.X
# code lines count about 70

import time
import os
from threading import Thread
from customTools.disguiser import user_agent
from customTools.loggerHome import novellogger
from customTools.databaseHome import novel_redis_client
from customTools.respDownloader import parse_target_urls
from customTools.queueHome import qiDianNovelElementQueue, qiDianNovelUrlQueue, qiDianNovelDataQueue
from dataHandler.NovelDataHandler_qiDian import qiDian_data_handler



class QiDianNovelSpider(object):
    """
    this is a spiders class for qiDian novel ,
    """

    def __init__(self):
        self.start_url = "https://www.qidian.com/rank/recom?dateType=2&chn=9&page={}"
        self.headers = {"User-Agent": user_agent()}

    def parse_list_urls(self):
        """
        :param urlQueue:        to give target url
        :param elementQueue:    to save the element of the page by parse url
        :param workLogger:      to record the work information
        :param redisClient:     save url finger print
        :param redisKey:        the redis data save key for url finger print
        :return:                None
        """
        while True:
            # every time to parse url use different User-Agent
            headers = {"User-Agent": user_agent(),"Connection":"close"}

            # use function import from customTools.respDownloader
            parse_target_urls(urlQueue=qiDianNovelUrlQueue,
                              elementQueue=qiDianNovelElementQueue,
                              headers=headers,
                              workLogger=novellogger,
                              redisClient=novel_redis_client,
                              redisKey="novel_url_finger")
            # print("url queue size:", qiDianNovelUrlQueue.qsize())

    def run(self):

        # create the target url list ,because the data we need is a rank,
        # so we don't need to get all data ,just top 100 is OK
        # each page has 20 data, we just need to parse page 1 to 5
        target_urls = [self.start_url.format(i) for i in range(1, 6)]

        # travers this target url list and add every one into url queue
        for url in target_urls:
            qiDianNovelUrlQueue.put(url)

        # try parse all url and get all page element add into the qiDianNovelEleQueue
        for i in range(3):
            t = Thread(target=self.parse_list_urls)
            t.setDaemon(True)
            t.setName("qiDianUrlParse{}".format(i))
            t.start()
            novellogger.info("threading which named {} begin to parse novel url".format(t.getName()))

        # start data handler
        time.sleep(5)
        qiDian_data_handler()

        for q in [qiDianNovelElementQueue, qiDianNovelUrlQueue, qiDianNovelDataQueue]:
            q.join()


if __name__ == '__main__':
    qidan = QiDianNovelSpider()
    qidan.run()
