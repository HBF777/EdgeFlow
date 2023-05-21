#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/6/10:54
# @Author  : 周伟帆
# @Project : edge-flow
# @File    : views
# @Software: PyCharm
"""
这里返回传感器数值
"""
from flask import jsonify
from . import sensor_bp
# from ..main import redis_helper
#保存传感器数据的字典
data_sensor = {
    "e_temperature":None,
    "e_humidity":None,
    "in_temperature":None,
    "in_humidity":None,
    "co2":None,
    "rain":None,
    "ex_red":None,
    "ex_visible":None,
    "ex_full":None,
    "in_red":None,
    "in_visible":None,
    "in_full":None
}

def get_data():
    global data_sensor
    """
    获取所有传感器的信息
    如何取？
    先判断是否有该key
        有的话取出来，没有的话 先置0
            
    :return: 
    """
    for key, value in data_sensor.items():
        print(key, ":", value)
        #将key取出来
        if redis_helper.is_existsKey(key):
            #存在
            data_sensor[key] = redis_helper.get(key)
        else:
            continue


#返回所有传感器信息
@sensor_bp.route('/server/allData')
def all_sensor_data():
    global data_sensor
    get_data()
    """
    获取到所有的传感器数值
    :return:
    """
    return_json = {
    "ext_Humiture": {
            "temperature": data_sensor["e_temperature"],
            "humidity": data_sensor["e_humidity"]
        },
    "builtin_Humiture": {
        "temperature": data_sensor["in_temperature"],
        "humidity": data_sensor["in_humidity"]
    },
    "co2": data_sensor["co2"],
    "rain": data_sensor["rain"],
    "ext_brightness": {
        "red": data_sensor["ex_red"],
        "visible": data_sensor["ex_visible"],
        "full": data_sensor["ex_full"]
        },
    "builtin_brightness": {
        "red": data_sensor["in_red"],
        "visible": data_sensor["in_visible"],
        "full": data_sensor["in_full"]
        }
    }
    return jsonify(return_json)

#返回gps定位
@sensor_bp.route('/server/gps')
def sensor_gps():
    global data_sensor
    """
    返回gps定位
    """
    return_json = {
        "gps": {
            "latitude": data_sensor["latitude"],
            "longitude": data_sensor["longitude"]
        }
    }
    return jsonify(return_json)
