#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/7 8:41
# @Author  : 李帅兵
# @FileName: redis_test.py
# @Software: PyCharm
from core.tools import RedisHelper

redis_client = RedisHelper()
redis_client.set("test", "2")
print(redis_client.get("test"))