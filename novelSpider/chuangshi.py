# -*- coding:utf-8 -*-
# python version= python3.X
# code lines count about 70
import os
from threading import Thread
from customTools.respDownloader import parse_target_urls, get_element
from customTools.disguiser import user_agent
from customTools.loggerHome import novellogger
from customTools.databaseHome import novel_redis_client
from customTools.queueHome import chuangShiNovelUrlQueue, chuangShiELementQueue, chuangShiDataQueue
from dataHandler.NovelDataHandler_chuangShi import chuangShi_data_handler

class ChuangShiNovelSpider(object):
    """
    this is a spiders class for novel information by chang shi wen xue website
    """

    def __init__(self):
        self.start_url = "http://chuangshi.qq.com/bang/tj/kh-week.html"

    def get_urls(self):
        """
        by parse start url to get detail urls for each book
        :return: detail url list
        """
        element = get_element(targetUrl=self.start_url, workLogger=novellogger, headers={"User-Agent": user_agent()})
        trs = element.xpath('.//tbody[@id="rankList"]//tr')[1:]
        for tr in trs:
            link = tr.xpath(".//a[@target='_blank']/@href")
            if len(link) > 0:
                chuangShiNovelUrlQueue.put(link[0])

    def parse_detail_url(self):

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
            headers = {"User-Agent": user_agent()}

            # use function import from customTools.respDownloader
            parse_target_urls(urlQueue=chuangShiNovelUrlQueue,
                              elementQueue=chuangShiELementQueue,
                              headers=headers,
                              workLogger=novellogger,
                              redisClient=novel_redis_client,
                              redisKey="novel_url_finger")
            # print("url queue size:", chuangShiNovelUrlQueue.qsize())

    def run(self):

        # parse start url and get detail urls ,add this detail urls into url queue
        self.get_urls()
        # try parse all detail url and add target element into element queue
        for i in range(10):
            t = Thread(target=self.parse_detail_url)
            t.setDaemon(True)
            t.setName("chuangShiUrlParse{}".format(i))
            t.start()
        # start data handlers
        chuangShi_data_handler()

        # join all queue
        for q in [chuangShiNovelUrlQueue, chuangShiELementQueue, chuangShiDataQueue]:
            q.join()


if __name__ == '__main__':
    chuangshi = ChuangShiNovelSpider()
    chuangshi.run()

