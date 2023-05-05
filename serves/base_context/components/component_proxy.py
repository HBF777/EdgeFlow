#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :component_proxy.py
# @Time      :2023/5/4 19:49
# @Author    :李帅兵
from abc import abstractmethod
from .abc_component import Sensor, Lamp


class ComponentProxy:
    def __init__(self, config, logger):
        self.logger = logger
        self.sensors = {}
        self.lamps = {}
        exec("from {impl} import *".format(impl=config['impl']))
        for item in config['sensor']:
            sensor = None
            try:
                sensor = eval("{component_object}(config = item,logger = logger)".format(
                    component_object=item['object']
                ))
                sensor.init()
                self.sensors[item['name']] = sensor
                self.logger.info("sensor {name} init success".format(name=item['name']))
            except Exception as e:
                self.logger.warning("sensor {name} init failed".format(name=item['name']))
                sensor.set_status(sensor.Abnormal)
                self.logger.warning(e)
        for item in config['lamp']:
            lamp = None
            try:
                lamp = eval("{component_object}(config = item,logger = logger)".format(
                    component_object=item['object']
                ))
                lamp.init()
                self.lamps[item['name']] = lamp
                self.logger.info("lamp {name} init success".format(name=item['name']))
            except Exception as e:
                self.logger.warning("lamp {name} init failed".format(name=item['name']))
                lamp.set_status(lamp.Abnormal)
                self.lamps[item['name']] = lamp
                self.logger.warning(e)

    def get_data(self, name):
        return self.sensors[name]

    def handle_lamp_light(self, name, data):
        self.lamps[name].set_light(data)

    def get_components_status(self):
        status = {}
        for name, sensor in self.sensors.items():
            status[name] = sensor.get_status()
        for name, lamp in self.lamps.items():
            status[name] = lamp.get_status()
        return status
