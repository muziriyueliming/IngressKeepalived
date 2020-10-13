#!/usr/bin/env python
# coding:utf-8
# zabbix钉钉报警
import hashlib, base64, urllib, hmac, requests, json, sys, os, datetime, time

dingding_token = os.getenv('ROBOT_TOKEN')
dingding_secret = os.getenv('SECRET')
dingding_text = sys.argv[1]


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
    except Exception as error:
        print(error)


if not dingding_token or not dingding_secret:
    print('you must set ROBOT_TOKEN or SECRET env')
    sys.exit(1)

send_alert(token=dingding_token, secret=dingding_secret, content=dingding_text)
