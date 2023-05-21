#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/8/21:05
# @Author  : 周伟帆
# @Project : zsciol-smartlamp-EdgeFlow-
# @File    : __init__.py
# @Software: PyCharm
from flask import Blueprint

gui_m_bp = Blueprint('gui_module', __name__)

from . import views
