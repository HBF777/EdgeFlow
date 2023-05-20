#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/14 7:40
# @Author  : 李帅兵
# @Project : Brilliant_Lamp_clustering
# @File    : testDriver.py
# @Software: PyCharm
import time

import RPi.GPIO as GPIO


class driver:
    def __init__(self,pins):
        GPIO.setmode(GPIO.BCM)
        self.a = pins['a']
        GPIO.setup(self.a, GPIO.OUT)

        print('初始化了a管脚:', self.a)

    def get_data(self):
        blinks = 0
        while blinks < 3:  # 闪烁5次
            GPIO.output(self.a, GPIO.HIGH)
            time.sleep(1.0)  # 延时1秒
            GPIO.output(self.a, GPIO.LOW)
            time.sleep(1.0)
            blinks = blinks + 1
        return self.a + 100
