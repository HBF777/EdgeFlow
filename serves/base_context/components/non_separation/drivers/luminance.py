#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/19 19:24
# @Author  : 李帅兵
# @Project : brilliant_clustering
# @File    : luminance.py
# @Software: PyCharm
from component.driver.baseDriver import Basedriver
from component.driver import brightness as brightness


class driver(Basedriver):
    def __init__(self, pins):
        self.sensor = None
        super().__init__(pins)

    def Init_pins(self):
        sensor = brightness.TSL2591()
        sensor.SET_InterruptThreshold(0xff00, 0x0010)

    def get_data(self):
        data = {
            "luminance":self.sensor.lux
        }
        return data
