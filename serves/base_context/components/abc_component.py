#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :abc_component.py
# @Time      :2023/5/5 10:06
# @Author    :李帅兵
from abc import abstractmethod

from core.tools import Logger


class Component(object):
    def __init__(self):
        self._status = None

    def living(self):
        pass

    def set_status(self, status):
        self._status = status


class Sensor(Component):
    Normal = 0
    Abnormal = 1
    ShutDown = 2

    def __init__(self, config):
        super().__init__()
        self._name = config['name']
        self.logger = Logger()
        self.config = config
        self._status = Sensor.Normal

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def get_data(self):
        pass

    def get_status(self):
        return self._status

    def get_name(self):
        return self._name

    @property
    def topic(self):
        return self.config['publish']


class Lamp(Component):
    Normal = 0
    Abnormal = 1
    ShutDown = 2

    def __init__(self, config):
        super().__init__()
        self._name = config['name']
        self._id = config['id']
        self.logger = Logger()
        self.config = config
        self._status = Lamp.Normal

    @abstractmethod
    def init(self):
        pass

    def get_status(self):
        return self._status

    def get_name(self):
        return self._name

    @abstractmethod
    def set_light(self, light):
        pass
