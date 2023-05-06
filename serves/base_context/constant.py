#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/4/28 23:26
# @Author  : 李帅兵
# @FileName: constant.py
# @Software: PyCharm

# 服务配置文件地址
COMPONENT_CONFIG_FILE_PATH = '/config/base_context/component_config.json'
COM_CONFIG_FILE_PATH = '/config/base_context/com_config.json'

REQ_TYPE_MQTT = "mqtt"
REQ_TYPE_LOCAL = "local"
# 消息等待最大次数
MESSAGE_WAIT_TIME = 77

# 管理器
MESSAGE_MANAGER = "MESSAGE_MANAGER"
TASK_MANAGER = "TASK_MANAGER"
HARD_MANAGER = "HARD_MANAGER"

# MQTT
NOT_CONNECT = 2
