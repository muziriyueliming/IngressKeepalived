# -*- coding:utf-8 -*-
import requests
from requests import HTTPError, RequestException
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import sys

LOG_DIR = "/tmp"
LOG_FILE = "ingress_health_check.log"
LOG_LEVEL = "INFO"

log_level = getattr(logging, LOG_LEVEL)
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR, 750)
RecodeLog = logging.getLogger("LOG INFO")
RecodeLog.setLevel(log_level)
# 建立一个filehandler来把日志记录在文件里，级别为debug以上
# 按天分割日志,保留30天
if not RecodeLog.handlers:
    fh = TimedRotatingFileHandler(
        os.path.join(LOG_DIR, LOG_FILE), when='D', interval=1, backupCount=30
    )
    ch = logging.StreamHandler()
    fh.setLevel(log_level)
    ch.setLevel(log_level)
    # 设置日志格式
    if LOG_LEVEL == "DEBUG":
        formatter = logging.Formatter(
            "%(asctime)s - Message of File(文件): %(filename)s,Module(类):%(module)s,FuncName(函数):%(funcName)s ,LineNo(行数):%(lineno)d - %(levelname)s - %(message)s"
        )
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    # 将相应的handler添加在logger对象中
    RecodeLog.addHandler(fh)
    RecodeLog.addHandler(ch)


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
            raise HTTPError(res.content)
        RecodeLog.info(msg="发送报警成功,url:{0},返回内容:{1}".format(url, res.content))
        sys.exit(0)
    except RequestException as error:
        RecodeLog.error(msg="发送报警失败,url:{0},返回内容:{1}".format(url, error))
        sys.exit(1)


health(url="http://11111/actuator/health", method="get")
