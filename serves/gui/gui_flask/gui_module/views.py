#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/8/21:06
# @Author  : 周伟帆
# @Project : zsciol-smartlamp-EdgeFlow-
# @File    : views
# @Software: PyCharm
from flask import jsonify
# from ..main import redis_helper
from . import gui_m_bp
"""
这里书写的是gui界面的其他模块
灯的控制与传感器之外的模块
"""
#保存设备状态的字典
device_information = {
    "lampNumber":None,
    "used":None,
    "speed":None,
    "all":None,
    "used_ed":None,
    "used_now":None,
    "readSpeed":None,
    "signal":None,
    "ipv4":None,
    "mode":None,
    "electricity":None,
    "voltage":None,
}

#写一个从数据库获取数据的方法
def get_data(service):
    #传入什么service，就去找什么数据
    #判断是否存在
    if redis_helper.is_existsKey(service):
        #存在
        return_data = redis_helper.get(service)
        return return_data
    else:
        return None




#获取灯杆编号
@gui_m_bp.route('/managerMsg/lampNumber')
def lampNumber():
    """
    获取灯杆编号
    :return:
    """
    lampNumber = get_data("lampNumber")
    return_json ={
        "lampNumber": lampNumber
    }
    return jsonify(return_json)

#获取cpu实时利用率以及Ghz速度
@gui_m_bp.route('/managerMsg/cpu')
def cpu():
    used = get_data("used")
    speed = get_data("speed")
    return_json ={
        "used": used,
        "speed": speed
    }
    return jsonify(return_json)

#获取实时内存使用率
@gui_m_bp.route('/managerMsg/cpu')
def cpu_memory():
    all = get_data("all")
    used = get_data("used_ed")
    return_json ={
        "all" : all,
        "used": used,
    }
    return jsonify(return_json)

#获取硬盘实时使用率以及读的速度
@gui_m_bp.route('/managerMsg/hardDisk')
def hardDisk():

    used = get_data("used_now")
    readSpeed = get_data("readSpeed")
    return_json ={
        "used": used,
        "readSpeed": readSpeed
    }
    return jsonify(return_json)

#获取硬盘实时使用率以及读的速度
@gui_m_bp.route('/managerMsg/WLAN')
def WLAN():
    signal = get_data("signal")
    ipv4 = get_data("ipv4")
    return_json ={
        "signal": signal,
        "ipv4": ipv4
    }
    return jsonify(return_json)


"""
工作模式切换
"""
@gui_m_bp.route("/changeMode")
def changeMode(mode):
    redis_helper.set("mode",mode)
    message = "success"
    return_json = {
        "message":message
    }
    return jsonify(return_json)

"控制系统的开关机"
@gui_m_bp.route("/switch/system")
def switch_systeme(type):
    control_type = type
    message = "success"
    return_json = {
        "message": message
    }
    return jsonify(return_json)

"设备的状态"
@gui_m_bp.route("/managerStatus")
def managerStatus(name):
    device = name
    status = None
    working = None
    return_json = {
        "status": status,
        "working": working
    }
    return jsonify(return_json)

"电压和电流"
@gui_m_bp.route('/manager/electricity')
def electricity():
    electricity = get_data("electricity")
    voltage = get_data("voltage")
    return_json ={
        "electricity": electricity,
        "voltage": voltage
    }
    return jsonify(return_json)


