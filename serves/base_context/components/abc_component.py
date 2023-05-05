#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :abc_component.py
# @Time      :2023/5/5 10:06
# @Author    :李帅兵
from abc import abstractmethod


class Sensor:
    Normal = 0
    Abnormal = 1
    ShutDown = 2

    def __init__(self, config, logger):
        self._name = config['name']
        self.logger = logger
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

    def set_status(self, status):
        self._status = status


class Lamp:
    Normal = 0
    Abnormal = 1
    ShutDown = 2

    def __init__(self, config, logger):
        self._name = config['name']
        self._id = config['id']
        self.logger = logger
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

    def set_status(self, status):
        self._status = status
