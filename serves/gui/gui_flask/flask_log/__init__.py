#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/8/21:26
# @Author  : 周伟帆
# @Project : zsciol-smartlamp-EdgeFlow-
# @File    : __init__.py
# @Software: PyCharm
from flask import Blueprint
log_bp = Blueprint('flask_log', __name__)
from . import views



