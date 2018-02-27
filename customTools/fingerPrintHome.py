# -*- coding:utf-8 -*-
# python version= python3.X
# code lines count about 60
from hashlib import md5


def _fingerprint(string):
    """
    the core of finger print functions
    :param string:
    :return: finger print string
    """
    # use sha1 or md5 ,because the result of md5 is shorter ,so we chose it.
    fp = md5(string.encode())
    finger = fp.hexdigest()
    # print(finger)
    return finger


def data_fingerprint(*args):
    """
    this is an data finger print maker
    :param args: data type must be 'string'
    :return: finger print string
    """
    data_tuple = args
    target_str = ""

    # check the data type if anyone is not belong to sting will raise an error information
    for item in data_tuple:
        data_type = type(item)
        if data_type is not str:
            raise PermissionError("the permission need be 'string' type but '{}' given".format(data_type))
        else:
            target_str += item
    return _fingerprint(target_str)


def _sort_url(url):
    """
    sort url to avoid request the same url repeat just because the query sort in url is different.
    :param url:
    :return: sorted url string
    """
    # if there is not query,just return url
    # because one url rote can must be in one sort rule
    if "?" not in url:
        return url
    url_splited = url.split("?")
    url_rote = url_splited[0]
    query_str = url_splited[1]
    # if there are many query key and value ,sort them, and then reset the url
    if "&" in query_str:
        query_list = query_str.split("&")
        query_list.sort()
        query_str = "&".join(query_list)
    url_sorted = url_rote + "?" + query_str
    return url_sorted


def url_fingerprint(url):
    """
    first to sort the url by '_sort_url',then create the finger print for this url
    :param url:
    :return: finger print string of url
    """
    url_sorted = _sort_url(url)
    return _fingerprint(url_sorted)


if __name__ == '__main__':
    # a = "nihao"
    # b = "xixi"
    # c = "haha"
    # finger_print = data_fingerprint(a, b, c)
    # print(finger_print)
    #
    # url1 = "http://blog.csdn.net/hechaoyuyu/article/details/6690912"
    # url2 = "https://www.baidu.com/s?ie=utf-8"
    # url3 = "https://www.baidu.com/s?ie=utf-8&f=3&rsv_bp=1&tn=baidu&wd=python%20%E8%8E%B7%E5%8F%96ascii&oq=python%2520%25E8%258E%25B7%25E5%258F%2596ascii&rsv_pq=907d8b15000122f4&rsv_t=fe65VoqsncMJTT3Ce0%2FRaVBNOGRR4CBd2DL1K47IA57Gs84yPjCuCr2IpMA&rqlang=cn&rsv_enter=0&prefixsug=python%2520%25E8%258E%25B7%25E5%258F%2596ascii&rsp=0"
    # urlsorted = _sort_url(url3)
    # print(urlsorted)
    pass
