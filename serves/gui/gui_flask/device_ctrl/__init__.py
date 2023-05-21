#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/13/11:00
# @Author  : 周伟帆
# @Project : zsciol-smartlamp-EdgeFlow-
# @File    : __init__.py
# @Software: PyCharm
from flask import Blueprint
device_bp = Blueprint('device_ctrl', __name__)
from . import views





