#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/4/28 23:26
# @Author  : 李帅兵
# @FileName: constant.py
# @Software: PyCharm
# 文件地址
LOG_FILE_PATH = '.log.BaseContextLog.log'
COM_CONFIG_FILE_PATH = 'config/base_context/com_config.json'
COMPONENT_CONFIG_FILE_PATH = "config/base_context/component_config.json"
# 服务名称
ComProxy_MESSAGE_LAMP = "ComProxy_MESSAGE_LAMP"
ComProxy_MESSAGE_SENSOR = "ComProxy_MESSAGE_SENSOR"
ComProxy_MESSAGE_SERVE = "ComProxy_MESSAGE_SERVE"
ComProxy_MESSAGE_WEBCAM = "ComProxy_MESSAGE_WEBCAM"
ComProxy_MESSAGE_EDGE_COMPUTING = "ComProxy_MESSAGE_EDGE_COMPUTING"

BASE_MESSAGE_CHANNEL = "BASE_MESSAGE_CHANNEL"
SERVE_MESSAGE_CHANNEL = "SERVE_MESSAGE_CHANNEL"
ComProxy_MESSAGE_GUI = "Gui"


# 消息等待最大次数
MESSAGE_WAIT_TIME = 77


# 管理器
MESSAGE_MANAGER = "MESSAGE_MANAGER"
TASK_MANAGER = "TASK_MANAGER"
HARD_MANAGER = "HARD_MANAGER"
