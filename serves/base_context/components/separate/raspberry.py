#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :raspberry.py
# @Time      :2023/5/5 10:12
# @Author    :李帅兵
from ..abc_component import Lamp as LampBase
from ..abc_component import Sensor as SensorBase


class Lamp(LampBase):
    def __init__(self, config, logger):
        super().__init__(config['name'])
        self.logger = logger

    def init(self):
        pass

    def get_name(self):
        pass

    def set_light(self, light):
        pass

    def set_status(self, status):
        pass