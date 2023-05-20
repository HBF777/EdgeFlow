#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/6/10:25
# @Author  : 周伟帆
# @Project : edge-flow
# @File    : run
# @Software: PyCharm
""""
此处编写flask启动程序，启动gui的后台只需要运行该程序的start方法即可
"""
# from core.tools import RedisHelper
from flask import Flask, Blueprint
from flask_cors import CORS
from .lamp import lamp_bp
from .sensor import sensor_bp
from .device_ctrl import device_bp
from .gui_module import gui_m_bp
#创建数据库对象
# redis_helper = RedisHelper()

app = Flask(__name__)
#解决跨域
# r'/*' 是通配符，让本服务器所有的 URL 都允许跨域请求
CORS(app,resources=r'/*')
# 注册蓝图
# app.register_blueprint(user_bp)

app.register_blueprint(lamp_bp)
app.register_blueprint(sensor_bp)
app.register_blueprint(device_bp)
app.register_blueprint(gui_m_bp)

def run():
    app.run(host="0.0.0.0", port=8000)

if __name__ == '__main__':
    run()


