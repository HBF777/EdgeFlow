#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :create_sensor_test.py
# @Time      :2023/5/5 10:54
# @Author    :李帅兵
from serves.base_context.components.non_separation.raspberry import *
from core.tools import ConfigParser
conf  = ConfigParser.parse_json("component_config.json")
sensors = {}
for item in conf['sensor']:
    try:
        sensor = eval("{component_object}(config = item,logger = None)".format(
            component_object=item['object']
        ))
        sensor.init()
        sensors[item['name']] = sensor
    except Exception as e:
        print(e)
        sensor.set_status(sensor.Abnormal)
        sensors[item['name']] = sensor
print(sensors)
