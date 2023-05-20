#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/13/11:01
# @Author  : 周伟帆
# @Project : zsciol-smartlamp-EdgeFlow-
# @File    : views
# @Software: PyCharm
from flask import jsonify
from flask import Flask, render_template, request, send_from_directory
import os
from flask_cors import *
from . import device_bp

"""
这里写入的是对于外接设备的控制
"""

#LED广告片
@device_bp.route('/upload')
@cross_origin(supports_credentials=True)
def upload():
    f = request.files['file']
    path = os.path.join('./upload', f.filename)
    f.save(path)
    # return render_template('upload.html')
    res = {}
    res['message'] = "success"
    return res