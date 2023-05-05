#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :test_time.py
# @Time      :2023/5/4 13:44
# @Author    :李帅兵
import time


x = time.time()
time.sleep(3)
y = time.time()
print(y-x)