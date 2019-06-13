#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import requests
import json
import socket

"""
monitor network status with open-falcon
"""

ts = int(time.time())
hostname = socket.gethostname()


def push_data_to_falcon():
    """
    通过ping检测网络连通性，并将数据push到falcon监控，网络可连通返回值为0
    :return: value
    """

    value = os.system("ping www.baidu.com -c 1 > /dev/null 2&>1")

    content = {
        "endpoint": hostname,
        "metric": "web_connect",
        "timestamp": ts,
        "step": 60,
        "value": value,
        "counterType": "GAUGE",
        "tags": "method=ping",
    }

    print(content)
    requests.post("http://127.0.0.1:1988/v1/push", data=json.dumps(content))


if __name__ == '__main__':
    push_data_to_falcon()




