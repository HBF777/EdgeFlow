#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/8/21:26
# @Author  : 周伟帆
# @Project : zsciol-smartlamp-EdgeFlow-
# @File    : views
# @Software: PyCharm
from flask import jsonify
from . import log_bp

def deal_log(log_data):
    """
    这里编写处理日志的方法

    :param log_data:
    :return:
    """
    log_list = []
    type1 = None
    time1 = None
    file1 = None
    info1 = None
    log_json = {

    }



#gui请求日志模块
@log_bp.route("/log")
def my_log():
    #返回日志
    log_data = None
    type1, time1, file1, info1 = deal_log(log_data)

