#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/6/10:25
# @Author  : 周伟帆
# @Project : edge-flow
# @File    : __init__.py
# @Software: PyCharm
from flask import Blueprint

sensor_bp = Blueprint('sensor', __name__)

from . import views