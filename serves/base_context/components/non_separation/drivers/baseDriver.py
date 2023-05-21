# -*- codeing = utf-8 -*-
# @Time : 2022/10/14 14:53
# @Autor: 李帅兵 202003024036
# @File : baseDriver.py
# @Software：PyCharm
import abc


class Basedriver(object):
    def __init__(self, pins):
        self.pins = pins
        self.Init_pins()

    @abc.abstractmethod
    def Init_pins(self):
        pass

    @abc.abstractmethod
    def get_data(self):
        pass
