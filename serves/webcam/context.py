#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/4/28 16:50
# @Author  : 李帅兵
# @FileName: context.py
# @Software: PyCharm
import os.path

from core.tools import Logger, ConfigParser
from .constant import *
from ..serves import BaseServerAbstract
from .haiKang.main import HKgo

webcam_config = None

def get_webcam_local_stream():
    """
    获取webcam配置文件 提供返回一个流的链接
    """
    pass


def start_webcam_stream():
    """
    启动webcam服务 和云端的连接
    """
    pass


def init_context():
    """
    初始化上下文
    """
    global webcam_config
    webcam_config = ConfigParser.parse_json(file_path=os.path.abspath(WEBCAM_CONFIG_FILE_PATH))
    #print(webcam_config)

class WebCamContext(BaseServerAbstract):
    def keep_alive(self):
        """
        心跳机制实现方法
        """
        while True:
            pass

    def await_get_message(self):
        """
        阻塞获取服务消息
        """
        pass

    def put_message(self):
        pass


    def __init__(self, *args, **kwargs):
        super(WebCamContext, self).__init__(*args, **kwargs)

    def run(self):
        """
        core启动方法，参数、服务的初始化、启动要在这里进行
        """
        # 初始化日志
        Logger(filename=LOG_FILE_NAME, level=LOG_LEVEL)
        # 日志使用
        Logger().info("WebCamContext init-ing..")
        # 初始化服务
        init_context()
        #启动
        HKgo()
        #self.keep_alive()
