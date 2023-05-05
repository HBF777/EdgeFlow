#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :file_path_test.py
# @Time      :2023/5/4 10:14
# @Author    :李帅兵
import os.path

from core.tools import Logger, ConfigParser
file_path = os.path.abspath("../config/base_context/com_config.json")
config = ConfigParser.parse_json(file_path=file_path)
t = Logger(filename="test.log")
t.logger.info("test")
