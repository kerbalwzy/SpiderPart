# -*- coding:utf-8 -*-
# python version= python3.X
# code lines count about 20

from fake_useragent import UserAgent


def user_agent():
    """
    this is an User-Agent string maker
    UserAgent().random can give an user agent string random
    :return: user agent string
    """
    default_user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
             Chrome/63.0.3239.84 Safari/537.36"
    try:
        random_user_agnet = UserAgent().random
    except Exception:
        return default_user_agent
    else:
        return random_user_agnet
