#!/usr/bin/env python
# coding:utf-8
# zabbix钉钉报警
import hashlib, base64, urllib, hmac, requests, json, sys, os, datetime, time
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import sys

dingding_token = os.getenv('ROBOT_TOKEN')
dingding_secret = os.getenv('SECRET')
dingding_text = sys.argv[1]

LOG_DIR = "/tmp"
LOG_FILE = "dingding.log"
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


def send_alert(token, content, secret):
    """
    :param token:
    :param content:
    :param secret:
    :return:
    """
    data = {
        "msgtype": "text",
        "text": {
            "content": content
        },
        "at": {
            "isAtAll": False
        }
    }

    headers = {'Content-Type': 'application/json'}
    timestamps = long(round(time.time() * 1000))
    url = "https://oapi.dingtalk.com/robot/send?access_token={0}".format(token)  # 说明：这里改为自己创建的机器人的webhook的值
    secret_enc = bytes(secret).encode('utf-8')
    to_sign = '{}\n{}'.format(timestamps, secret)
    to_sign_enc = bytes(to_sign).encode('utf-8')
    hmac_code = hmac.new(secret_enc, to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.quote_plus(base64.b64encode(hmac_code))
    url = "{0}&timestamp={1}&sign={2}".format(url, timestamps, sign)
    try:
        x = requests.post(url=url, data=json.dumps(data), headers=headers)
        if x.json()["errcode"] != 0:
            raise Exception(x.content)
        RecodeLog.info(msg="发送报警成功,url:{0},报警内容:{1}".format(url, data))
    except Exception as error:
        RecodeLog.info(msg="发送报警失败,url:{0},报警内容:{1},原因:{2}".format(url, data, error))


if not dingding_token or not dingding_secret:
    print('you must set ROBOT_TOKEN or SECRET env')
    sys.exit(1)

send_alert(token=dingding_token, secret=dingding_secret, content=dingding_text)
