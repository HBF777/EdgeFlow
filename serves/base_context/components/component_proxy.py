#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :component_proxy.py
# @Time      :2023/5/4 19:49
# @Author    :李帅兵
from abc import abstractmethod

from core.constant import Message, SENSOR_DATA_REDIS_KEY
from core.tools import Logger, RedisHelper
from .abc_component import Sensor, Lamp


class ComponentProxy:
    def __init__(self, config):
        self.sensors = {}
        self.lamps = {}
        exec("from {impl} import *".format(impl=config['impl']))
        for item in config['sensor']:
            sensor = None
            try:
                sensor = eval("{component_object}(config = item)".format(
                    component_object=item['object']
                ))
                sensor.init()
                self.sensors[item['name']] = sensor
                Logger().info("sensor {name} init success".format(name=item['name']))
            except Exception as e:
                Logger().warning("sensor {name} init failed".format(name=item['name']))
                sensor.set_status(sensor.Abnormal)
                Logger().warning(e)
        for item in config['lamp']:
            lamp = None
            try:
                lamp = eval("{component_object}(config = item)".format(
                    component_object=item['object']
                ))
                lamp.init()
                self.lamps[item['name']] = lamp
                Logger().info("lamp {name} init success".format(name=item['name']))
            except Exception as e:
                Logger().warning("lamp {name} init failed".format(name=item['name']))
                lamp.set_status(lamp.Abnormal)
                self.lamps[item['name']] = lamp
                Logger().warning(e)

    def get_data_topic(self, message: Message)->Message:
        try:
            message.message_data = self.sensors[message.target_obj].get_data()
            message.message_type = Message.TYPE_DATA_HARD
            message.message_to, message.message_from = message.sender, message.receiver
            message.message_topic = self.sensors[message.target_obj].topic
            return message
        except Exception as e:
            Logger().warning(e)
            raise e

    def get_data_names(self, message) -> Message:
        res = {}
        if message.target_obj == Message.ALL_SENSOR:
            for name, sensor in self.sensors.items():
                res[name] = sensor.get_data()
        elif message.target_obj == Message.ALL_LAMP:
            for name, lamp in self.lamps.items():
                res[name] = lamp.get_data()
        RedisHelper().set(SENSOR_DATA_REDIS_KEY, str(res))
        message.message_data = res
        message.message_type = Message.TYPE_DATA_HARD
        message.message_to, message.message_from = message.sender, message.receiver
        return message

    def handle_lamp_light(self, name, data):
        self.lamps[name].set_light(data)

    def get_components_status(self):
        status = {}
        for name, sensor in self.sensors.items():
            status[name] = sensor.get_status()
        for name, lamp in self.lamps.items():
            status[name] = lamp.get_status()
        return status

    def living(self):
        for name, sensor in self.sensors.items():
            sensor.living()
        for name, lamp in self.lamps.items():
            lamp.living()
