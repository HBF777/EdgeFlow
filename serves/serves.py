#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/4/29 2:54
# @Author  : 李帅兵
# @FileName: serves.py
# @Software: PyCharm
import abc


class BaseServerAbstract:
    def __init__(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def keep_alive(self):
        pass

    @abc.abstractmethod
    def await_get_message(self):
        pass

    @abc.abstractmethod
    def put_message(self):
        pass

    @staticmethod
    def parse_serve_message(message):
        pass
