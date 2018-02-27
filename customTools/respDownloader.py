# -*- coding:utf-8 -*-
# python version= python3.X
# code lines count about 80

import requests
from retrying import retry
from lxml import etree
import time


from customTools.fingerPrintHome import url_fingerprint

# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context

_session = requests.session()



@retry(stop_max_attempt_number=10)
def parse_url(targetUrl, headers, workLogger):
    """
    try request the url ,time out is 5 second, retry 3 time max

    :param targetUrl:       the url we want parse
    :param headers:         the request headers
    :param workLogger:      the logger project
    :return: response project
    """
    try:
        response = _session.get(url=targetUrl, headers=headers, verify=False, timeout=5)
    except Exception as e:
        workLogger.error(e)
        time.sleep(5)
        raise e
    else:
        workLogger.info("parse url:{} and get response successful".format(targetUrl))
        return response


def check_url(targetUrl, redisClient, redisKey):
    """
    check the url if had requested,

    :param targetUrl:       the url we want parse
    :param redisClient:     redis database worker
    :param redisKey:        data save key
    :return: true or false
    """
    url_finger = url_fingerprint(url=targetUrl)
    result = redisClient.sadd(redisKey, url_finger)
    return True if result == 1 else False


def get_element(targetUrl, workLogger, headers):
    """
    get the element of current html text get from the url

    :param targetUrl:       the url we need parse
    :param workLogger:      the logger project to record information
    :return: element
    """
    response = parse_url(targetUrl=targetUrl, headers=headers, workLogger=workLogger, )
    element = etree.HTML(response.text)
    return element


def parse_target_urls(urlQueue, elementQueue, headers, workLogger, redisClient, redisKey):
    """
    get url from the url queue,and request it to get element
    add the element into the element queue ,waite for get data

    :param urlQueue:        to give target url
    :param elementQueue:    to save the element of the page by parse url
    :param workLogger:      to record the work information
    :param redisClient:     save url finger print
    :param redisKey:        the redis data save key
    :return: None
    """
    url = urlQueue.get()
    if check_url(url, redisClient=redisClient, redisKey=redisKey):
        element = get_element(targetUrl=url, headers=headers, workLogger=workLogger)
        elementQueue.put(element)
    urlQueue.task_done()
