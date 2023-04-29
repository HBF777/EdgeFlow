#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/4/28 16:50
# @Author  : 李帅兵
# @FileName: context.py
# @Software: PyCharm
from ..serves import BaseServerAbstract


class GuiContext(BaseServerAbstract):
    def __init__(self, *args, **kwargs):
        super(GuiContext, self).__init__()

    def keep_alive(self):
        pass

    def await_get_message(self):
        pass

    def put_message(self):
        pass
