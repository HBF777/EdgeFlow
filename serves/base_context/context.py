#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/4/28 16:50
# @Author  : 李帅兵
# @FileName: context.py
# @Software: PyCharm
import os.path
import time
from core.constant import *
from .constant import *
from ..serves import BaseServerAbstract
from core.tools import Logger

logger = None


class BaseContext(BaseServerAbstract):
    def __init__(self, *args, **kwargs):
        super(BaseContext, self).__init__(*args, **kwargs)
        self.base_path = None

    def run(self):
        global logger
        self.base_path = os.path.abspath(".")
        logger = Logger(filename=self.base_path + LOG_FILE_PATH, level="debug")
        while True:
            self.send_queue.put(TestMessage())
            time.sleep(1)
        pass

    def keep_alive(self):
        pass

    def await_get_message(self):
        pass

    def put_message(self):
        pass
