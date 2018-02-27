# -*- coding:utf-8 -*-
# python version= python3.X
# code lines count about 40

from customTools.databaseHome import music_redis_client, novel_redis_client, music_mongo_clinet, novel_mongo_clinet

from videoSpider.weibo import WeiboVideoSpider
from musicSpider.cloudmusic import CloudMusicSpider
from novelSpider.chuangshi import ChuangShiNovelSpider
from novelSpider.qidian import QiDianNovelSpider


# create spider object
video = WeiboVideoSpider()
music = CloudMusicSpider()
novel1 = QiDianNovelSpider()
novel2 = ChuangShiNovelSpider()

def init_dbs():
    # clear redis database and mongodb collections of music and novel
    music_redis_client.flushdb()
    novel_redis_client.flushdb()
    music_mongo_clinet.drop()
    novel_mongo_clinet.drop()

# define spider start function
def video_spider():
    video.run()

def music_spider():
    music.run()

def novel_spider_1():
    novel1.run()

def novel_spider_2():
    novel2.run()


if __name__ == '__main__':
    init_dbs()
    video_spider()
    music_spider()
    novel_spider_1()
    novel_spider_2()
