#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/4/28 17:14
# @Author  : 李帅兵
# @FileName: constantTst.py
# @Software: PyCharm
from core.constant import ServerConstant
print(ServerConstant.BASE_CONTEXT_NAME)
ServerConstant.ABC = "ww"
print(ServerConstant.ABC)