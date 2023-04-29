#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/4/28 16:46
# @Author  : 李帅兵
# @FileName: constant.py
# @Software: PyCharm
CONFIG_FILE_PATH = '/config/core/app_config.json'
LOGGER_FILE_PATH = '/core/log/logfile.log'
LOGGER_LEVEL = 'debug'
SERVE_QUEUE_SIZE = 77


class ServerConstant:
    # 基础服务名称
    DEVICE_ID = None
    BASE_CONTEXT_NAME = 'BaseContext'
    # GUI服务名称
    GUI_CONTEXT_NAME = 'Gui'
    # 摄像头服务名称
    WEBCAM_CONTEXT_NAME = 'WebCam'
    # 边缘计算服务名称
    EDGE_COMPUTING_CONTEXT_NAME = 'EdgeComputing'
