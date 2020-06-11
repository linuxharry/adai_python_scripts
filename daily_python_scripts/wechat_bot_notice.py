#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
发送微信机器人消息提醒！
"""
import requests
import sys

token = u'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=aca0ef08-9f7e-4fb9-a0cc-62686b6d637d'


def build_text(text):
    return {
        "msgtype": "text",
        "text": {
            "content": text or u'',
            "mentioned_mobile_list": ["", "@all"]  # 强制提醒，@所有人
        },
    }


def post_webhook(token, content):
    try:
        # print(content)  # debug
        response = requests.post(token, json=content, timeout=2)
        return response.status_code == 200
    except:
        return False


def send_text(token, text):
    """
    发送文本
    """
    notice = build_text(text)
    return post_webhook(token, notice)


if __name__ == '__main__':
    text = sys.argv[1]
    send_text(token, text)


