#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/6/10:34
# @Author  : 周伟帆
# @Project : edge-flow
# @File    : views
# @Software: PyCharm
"""
这里对路灯进行控制
"""
from flask import jsonify
from ..main import redis_helper
from . import lamp_bp

"""
路灯开关
"""
#主
#开
@lamp_bp.route('/server/lamp/turnOn/003')
def turn_on_main_lamp():
    """
    开启主灯
    :return:
    """
    status = True
    return_json ={
        "status": status
    }
    return jsonify(return_json)

#关
@lamp_bp.route('/server/lamp/turnOff/003')
def turn_off_main_lamp():
    """
    开启主灯
    :return:
    """
    status = True
    return_json ={
        "status": status
    }
    return jsonify(return_json)

#从1
#开
@lamp_bp.route('/server/lamp/turnOn/001')
def turn_on_001_lamp():
    """
    开启从灯1
    :return:
    """
    status = True
    return_json ={
        "status": status
    }
    return jsonify(return_json)

#关
@lamp_bp.route('/server/lamp/turnOff/001')
def turn_off_001_lamp():
    """
    关闭从灯1
    :return:
    """
    status = True
    return_json ={
        "status": status
    }
    return jsonify(return_json)

#从2
#开
@lamp_bp.route('/server/lamp/turnOn/002')
def turn_on_002_lamp():
    """
    开启从灯2
    :return:
    """
    status = True
    return_json ={
        "status": status
    }
    return jsonify(return_json)

#关
@lamp_bp.route('/server/lamp/turnOff/002')
def turn_off_002_lamp():
    """
    关闭从灯2
    :return:
    """
    status = True
    return_json ={
        "status": status
    }
    return jsonify(return_json)


"""
路灯调光
"""
#主
#调亮
@lamp_bp.route('/server/lamp/setLightUp/003')
def set_light_up_main():
    """
    增加主灯亮度
    :return:
    """
    brightness = 60
    return_json = {
        "brightness": brightness
    }
    return jsonify(return_json)

#调暗
@lamp_bp.route('/server/lamp/setLightDown/003')
def set_light_down_main():
    """
    降低主灯亮度
    :return:
    """
    brightness = 60
    return_json = {
        "brightness": brightness
    }
    return jsonify(return_json)

#从1
#调亮
@lamp_bp.route('/server/lamp/setLightUp/001')
def set_light_up_001():
    """
    增加从灯1亮度
    :return:
    """
    brightness = 60
    return_json = {
        "brightness": brightness
    }
    return jsonify(return_json)

#调暗
@lamp_bp.route('/server/lamp/setLightDown/001')
def set_light_down_001():
    """
    降低从灯1亮度
    :return:
    """
    brightness = 60
    return_json = {
        "brightness": brightness
    }
    return jsonify(return_json)

#从2
#调亮
@lamp_bp.route('/server/lamp/setLightUp/002')
def set_light_up_002():
    """
    增加从灯2亮度
    :return:
    """
    brightness = 60
    return_json = {
        "brightness": brightness
    }
    return jsonify(return_json)

#调暗
@lamp_bp.route('/server/lamp/setLightDown/002')
def set_light_down_002():
    """
    降低从灯2亮度
    :return:
    """
    brightness = 60
    return_json = {
        "brightness": brightness
    }
    return jsonify(return_json)


#############################
#一下是带参数的请求
############################

#开关调节
@lamp_bp.route('/server/lamp/turnOn')
def turn_on_lamp(lamp_number):
    ##开启第 lamp_number 个灯
    status = "success"
    return_json = {
        "status": status
    }
    return jsonify(return_json)

@lamp_bp.route('/server/lamp/turnOff')
def turn_on_lamp(lamp_number):
    ##关闭第 lamp_number 个灯
    status = "success"
    return_json = {
        "status": status
    }
    return jsonify(return_json)


#亮度调节
@lamp_bp.route('/server/lamp/setLightUp')
def setLightUp(lamp_number):
    status = "success"
    brightness = 12
    return_json = {
        "status": status,
        "brightness":brightness
    }
    return jsonify(return_json)

@lamp_bp.route('/server/lamp/setLighttDown')
def setLightDown(lamp_number):
    status = "success"
    brightness = 12
    return_json = {
        "status": status,
        "brightness":brightness
    }
    return jsonify(return_json)


#光照阈值设定


#定时开关

