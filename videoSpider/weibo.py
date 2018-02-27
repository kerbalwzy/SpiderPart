# -*- coding:utf-8 -*-
# python version= python3.X
# code lines count about 100
import os
import time
import requests
from retrying import retry
from customTools.loggerHome import videologger
from dataHandler.videoDataHandler import data_hander_and_save

"""
target text demo:
video source:
video-sources=\"fluency=http%253A%252F%252Fgslb.miaopai.com%252Fstream%252FICwfXDM-noKaPBF%7Ef1ove9bLiKFnOdmZwNpl
MA__.mp4%253Fyx%253D%2526refer%253Dweibo_app%2526Expires%253D1514177981%2526ssig%253D3%25252BLHcxOEuW%2526KID%253D
unistore%252Cvideo&480=http%3A%2F%2Fgslb.miaopai.com%2Fstream%2FICwfXDM-noKaPBF~f1ove9bLiKFnOdmZwNplMA__.mp4%3Fyx%
3D%26refer%3Dweibo_app%26Expires%3D1514177981%26ssig%3D3%252BLHcxOEuW%26KID%3Dunistore%2Cvideo&720=&qType=480\"
poster image source:
src=\"\/\/dslb.cdn.krcom.cn\/stream\/JBJ9axkL4NRRgDC6bsUkzQSJ851e46gGbDvNOA___32768.jpg\"
"""


class WeiboVideoSpider(object):
    """this is spiders class for weibo to get video source"""

    def __init__(self):
        self.start_url = "https://weibo.com/u/5644848255?is_all=1"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
             Chrome/63.0.3239.84 Safari/537.36",
        }
        self.session = requests.session()
        self.cookies = "YF-Page-G0={}; SUB=_2AkMtHC_nf8NxqwJRmPEXzW3lZYpywgzEieKbQN48JRMxHRl-yT9kqhYAtRB6\
        BpwBCHKyz1KAM7nViR4l5X5CkqHaJ5QP; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W5qu3mLeGn15mePAZBb6miL"

    @retry(stop_max_attempt_number=3)
    def parse_url(self, target_url):
        try:
            response = self.session.get(url=target_url, headers=self.headers, timeout=5)
        except Exception as e:
            videologger.error(e)
            raise e
        else:
            videologger.info("parse url {} and get response successful!, ".format(target_url))
            return response

    def get_cookies(self):
        cookie = self.session.cookies.get_dict()
        return cookie["YF-Page-G0"]

    def get_html_text(self, response):
        html_text = response.text
        return html_text

    def run(self):

        # request the url to get the cookie we need for visit really page source
        videologger.info("video spiders begin to run")
        self.parse_url(self.start_url)
        videologger.info("parse url to get cookie")
        time.sleep(1)
        # set new cookie information and insert to headers
        try:
            cookie = self.get_cookies()
            videologger.info("get cookie successful, the key cookie is {}".format(cookie))
            self.cookies.format(cookie)
            self.headers["Cookie"] = self.cookies
            videologger.info("format cookie into request headers successful")
        except Exception as e:
            videologger.error(e)
            raise e

        # request the url to get page html text
        response = self.parse_url(self.start_url)
        html_text = self.get_html_text(response)
        videologger.info("parse url to get response content string for data successful")
        data_hander_and_save(html_text)


if __name__ == '__main__':
    video = WeiboVideoSpider()
    video.run()
