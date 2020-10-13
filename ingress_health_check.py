# -*- coding:utf-8 -*-
import requests
from requests import HTTPError, RequestException
import sys


def health(url, method):
    """
    :param url:
    :param method:
    :return:
    """
    if method not in ['get', 'post', 'put']:
        raise Exception("请求格式错误")

    try:
        res = requests.request(method=method, url=url, timeout=3)
        if res.status_code != 200:
            raise HTTPError("连接状态异常!状态:{0},报错信息:{1}".format(res.status_code, res.reason))
        sys.exit(0)
    except RequestException as error:
        print(error)
        sys.exit(1)


health(url="http://10.253.100.12:80", method="post")
