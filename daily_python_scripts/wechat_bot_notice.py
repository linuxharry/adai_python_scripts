#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
发送微信机器人消息提醒！
TO DO: 替换 text 信息为 args
"""
import requests

token = u'xxxxxxx'


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
    text = u'温馨提示：施主，xxxxx?'
    send_text(token, text)


