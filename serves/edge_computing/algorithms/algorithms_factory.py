#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/21 18:45
# @Author  : 李帅兵
# @FileName: algorithms_factory.py
# @Software: PyCharm
import abc


class Algorithm(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractmethod
    def execute(self):
        pass

    @staticmethod
    def set_lightness(self):
        pass

    def get_distance(self, method):
        pass

    def get_brightness(self):
        pass


class algo_factory:

    def __init__(self):
        pass

    def get_algo(self):
        pass
