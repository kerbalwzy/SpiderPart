# -*- coding:utf-8 -*-
# python version= python3.X
# code lines count about 100

from redis import StrictRedis
from pymongo import MongoClient
from customTools.setting import REDIS_HOST_FOR_MUSIC, REDIS_PORT_FOR_MUSIC, REDIS_NUM_FOR_MUSIC
from customTools.setting import REDIS_HOST_FOR_VIDEO, REDIS_PORT_FOR_VIDEO, REDIS_NUM_FOR_VIDEO
from customTools.setting import REDIS_HOST_FOR_NOVEL, REDIS_PORT_FOR_NOVEL, REDIS_NUM_FOR_NOVEL

from customTools.setting import MONGO_HOST_FOR_VIDEO, MONGO_PORT_FOR_VIDEO, DATABASE_NAME_FOR_VIDEO, \
    COLLECTIOIN_NAME_FOR_VIDEO
from customTools.setting import MONGO_HOST_FOR_NOVEL, MONGO_PORT_FOR_NOVEL, DATABASE_NAME_FOR_NOVEL, \
    COLLECTIOIN_NAME_FOR_NOVEL
from customTools.setting import MONGO_HOST_FOR_MUSIC, MONGO_PORT_FOR_MUSIC, DATABASE_NAME_FOR_MUSIC, \
    COLLECTIOIN_NAME_FOR_MUSIC


class _MyRedis(object):
    """this is a basic class for redis client"""

    def __init__(self, host="127.0.0.1", port=6379, database=0):
        """default host ,port and database number"""
        self._host = host
        self._port = port
        self._database = database

    def _connect_redis(self):
        """when you chose to connect to redis ,there will return a redis client by default initially
            and then you can use this object to operate the redis database you chose
        """
        return StrictRedis(host=self._host, port=self._port, db=self._database)


class _MyRedisForVidoe(_MyRedis):
    def __init__(self):
        super().__init__(host=REDIS_HOST_FOR_VIDEO,
                         port=REDIS_PORT_FOR_VIDEO,
                         database=REDIS_NUM_FOR_VIDEO)


class _MyRedisForMusic(_MyRedis):
    def __init__(self):
        super().__init__(host=REDIS_HOST_FOR_MUSIC,
                         port=REDIS_PORT_FOR_MUSIC,
                         database=REDIS_NUM_FOR_MUSIC)


class _MyRedisForNovel(_MyRedis):
    def __init__(self):
        super().__init__(host=REDIS_HOST_FOR_NOVEL,
                         port=REDIS_PORT_FOR_NOVEL,
                         database=REDIS_NUM_FOR_NOVEL)


class _MyMongoDB(object):
    """this is a basic class for mongodb client"""

    def __init__(self, host="127.0.0.1", port=27017, database_name="test_db", collection_name="test_collection"):
        self.host = host
        self.port = port
        self.database_name = database_name
        self.collection_name = collection_name

    def _connect_mongo(self):
        client = MongoClient(host=self.host, port=self.port)
        return client[self.database_name][self.collection_name]


class _MyMongoForNovel(_MyMongoDB):
    def __init__(self):
        super().__init__(
            host=MONGO_HOST_FOR_NOVEL,
            port=MONGO_PORT_FOR_NOVEL,
            database_name=DATABASE_NAME_FOR_NOVEL,
            collection_name=COLLECTIOIN_NAME_FOR_NOVEL)


class _MyMongoForVideo(_MyMongoDB):
    def __init__(self):
        super().__init__(
            host=MONGO_HOST_FOR_VIDEO,
            port=MONGO_PORT_FOR_VIDEO,
            database_name=DATABASE_NAME_FOR_VIDEO,
            collection_name=COLLECTIOIN_NAME_FOR_VIDEO)


class _MyMongoForMusic(_MyMongoDB):
    def __init__(self):
        super().__init__(
            host=MONGO_HOST_FOR_MUSIC,
            port=MONGO_PORT_FOR_MUSIC,
            database_name=DATABASE_NAME_FOR_MUSIC,
            collection_name=COLLECTIOIN_NAME_FOR_MUSIC)


# create video clients for redis and mongodb
_redis_maker = _MyRedisForVidoe()
video_redis_client = _redis_maker._connect_redis()

_mongo_maker = _MyMongoForVideo()
video_mongo_clinet = _mongo_maker._connect_mongo()

# create music clients for redis and mongodb
_redis_maker = _MyRedisForMusic()
music_redis_client = _redis_maker._connect_redis()

_mongo_maker = _MyMongoForMusic()
music_mongo_clinet = _mongo_maker._connect_mongo()

# create novel clients for redis and mongodb
_redis_maker = _MyRedisForNovel()
novel_redis_client = _redis_maker._connect_redis()

_mongo_maker = _MyMongoForNovel()
novel_mongo_clinet = _mongo_maker._connect_mongo()

if __name__ == '__main__':
    # redismaker = _MyRedis()
    # redisclient = redismaker._connect_redis()
    # redisclient.set("test","test value")
    # mongomaker = _MyMongoDB()
    # mongoclient = mongomaker._connect_mongo()
    # mongoclient.insert_one("this is a test data")
    pass
