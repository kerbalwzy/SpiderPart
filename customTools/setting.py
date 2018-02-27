# -*- coding:utf-8 -*-
# python version= python3.X
# code lines count about 40

# this is the setting page for this spiders system to connect with databases,
# all setting is must be!

# chose which redis database for video spiders
# default value like down content
REDIS_HOST_FOR_VIDEO = "127.0.0.1"
REDIS_PORT_FOR_VIDEO = 6379
REDIS_NUM_FOR_VIDEO = 1

# set mongoDB config for video spiders
# default value like down content
MONGO_HOST_FOR_VIDEO = "127.0.0.1"
MONGO_PORT_FOR_VIDEO = 27017
DATABASE_NAME_FOR_VIDEO = "video"
COLLECTIOIN_NAME_FOR_VIDEO = "weibo"


# chose which redis database for music spiders
# default value like down content
REDIS_HOST_FOR_MUSIC = "127.0.0.1"
REDIS_PORT_FOR_MUSIC = 6379
REDIS_NUM_FOR_MUSIC = 2

# set mongoDB config for music spiders
# default value like down content
MONGO_HOST_FOR_MUSIC = "127.0.0.1"
MONGO_PORT_FOR_MUSIC = 27017
DATABASE_NAME_FOR_MUSIC = "music"
COLLECTIOIN_NAME_FOR_MUSIC = "wangyicloud"


# chose which redis database for novel spiders
# default value like down content
REDIS_HOST_FOR_NOVEL = "127.0.0.1"
REDIS_PORT_FOR_NOVEL = 6379
REDIS_NUM_FOR_NOVEL = 3

# set mongoDB config for novel spide
# default value like down content
MONGO_HOST_FOR_NOVEL = "127.0.0.1"
MONGO_PORT_FOR_NOVEL = 27017
DATABASE_NAME_FOR_NOVEL = "novel"
COLLECTIOIN_NAME_FOR_NOVEL = "all"

