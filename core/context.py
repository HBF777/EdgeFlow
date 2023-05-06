#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/4/28 17:15
# @Author  : 李帅兵
# @FileName: context.py
# @Software: PyCharm
import abc
import platform
import os
import time
import traceback
import sys
from multiprocessing import Process, Queue, freeze_support

from core.constant import *
from core.tools import Logger, ConfigParser
from serves.base_context.context import BaseContext
from serves.edge_computing.context import EdgeComputingContext
from serves.gui.context import GuiContext


class ProcessBaseServe(Process):
    def __init__(self, *args, **kwargs):
        super(ProcessBaseServe, self).__init__()
        self.__activate = self.__create_service_impl(device_id=kwargs['device_id'],
                                                     send_queue=kwargs['send_queue'],
                                                     recv_queue=kwargs['recv_queue'],
                                                     service_impl=kwargs['service_impl'])

    def await_get_message(self):
        pass

    def put_message(self):
        pass

    def run(self):
        self.service.run()

    def __create_service_impl(self, *args, **kwargs):
        try:
            self.service = kwargs['service_impl'](*args, **kwargs)
        except OSError as e:
            raise NotImplementedError
        return True


def check_dependent_environment(*args, **kwargs):
    print("检查系统环境")
    print("当前处理器架构为", platform.machine())
    print("当前处理器类型为", platform.processor())
    print("当前操作系统为", platform.system())
    print("当前操作系统版本为", platform.version())
    print("当前操作系统位数为", platform.architecture())
    print("当前设备Uart已开启")
    print("当前设备I2C已开启")
    print("当前设备SPI已开启")
    print("当前设备GPIO已开启")
    print("当前设备PWM已开启")


class App:
    class BaseContext(ProcessBaseServe):
        def __init__(self, *args, **kwargs):
            kwargs['service_impl'] = BaseContext
            super().__init__(*args, **kwargs)

    class EdgeComputing(ProcessBaseServe):
        def __init__(self, *args, **kwargs):
            kwargs['service_impl'] = EdgeComputingContext
            super().__init__(*args, **kwargs)

    class Gui(ProcessBaseServe):
        def __init__(self, *args, **kwargs):
            kwargs['service_impl'] = GuiContext
            super().__init__(*args, **kwargs)

    class WebCam(ProcessBaseServe):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        base_path = os.path.abspath(".")
        # 初始化日志
        self.logger = Logger(filename=base_path + LOGGER_FILE_PATH, level=LOGGER_LEVEL).logger
        self.last_start_time = time.time()
        # 初始化配置文件
        self.logger.info("初始化配置文件")
        self.config = ConfigParser.parse_json(file_path=base_path + CONFIG_FILE_PATH)
        ServerConstant.DEVICE_ID = self.config['device_id']
        # 检查系统环境
        self.logger.info("检查系统环境")
        check_dependent_environment()
        # 初始化服务
        self.serves = {}
        self.init_service()

    def init_service(self, *args, **kwargs):
        """
        初始化服务,创建服务实例
        :param args:
        :param kwargs:
        :return:
        """
        for serve in self.config['serves']:
            serve_name = serve['serve_name']
            self.logger.info("正在激活" + serve_name + "服务---->")
            recv_queue = Queue(SERVE_QUEUE_SIZE)
            send_queue = Queue(SERVE_QUEUE_SIZE)
            # 对于core来说，其发送队列，在服务的角度看是接收队列
            serve_impl = eval("App.{serveImpl}(device_id=ServerConstant.DEVICE_ID,send_queue=recv_queue,"
                              "recv_queue=send_queue) "
                              .format(serveImpl=serve['serve_name']))
            self.serves[serve_name] = {
                "serve": serve_impl,
                "send_queue": send_queue,
                "recv_queue": recv_queue
            }

    def run(self):
        """
        启动服务
        :return:
        """
        self.logger.info("启动服务")
        for serve_name, serve in self.serves.items():
            self.logger.info("启动" + serve_name + "服务")
            serve['serve'].start()
        self.logger.info("服务启动完成")
        time.sleep(1)
        self.logger.info("启动服务监听")
        self.listen_serves()

    def listen_serves(self):
        while True:
            # 查看子进程状态
            for serve_name, serve in self.serves.items():
                if not serve['serve'].is_alive():
                    self.logger.error(serve_name + "服务异常退出")
                    if serve_name == ServerConstant.BASE_CONTEXT_NAME:
                        self.logger.error("基础服务异常退出，尝试重启")
                        sys.exit(1) if self.deal_base_context_exception() else None
                    else:
                        self.logger.error(serve_name + "服务异常退出，尝试重启")
                        serve['serve'].terminate()
                        recv_queue = Queue(SERVE_QUEUE_SIZE)
                        send_queue = Queue(SERVE_QUEUE_SIZE)
                        serve['serve'] = eval("App.{serveImpl}(device_id=ServerConstant.DEVICE_ID,"
                                              "send_queue=send_queue, "
                                              "recv_queue=recv_queue) "
                                              .format(serveImpl=serve_name))
                        serve['serve'].start()
                        serve['send_queue'] = send_queue
                        serve['recv_queue'] = recv_queue
                        self.serves[serve_name] = serve
                    continue
                if serve['recv_queue'].empty():
                    continue
                self.message_handler(serve['recv_queue'].get())

    def message_handler(self, message: Message):
        if message.is_to_core_control_self:  # 检查是否是服务操作自己的消息 如何自我服务重启，自我服务停止
            pass
        elif message.receiver in self.serves:
            self.serves.get(message.receiver).get("send_queue").put(message)
        else:
            self.logger.error("接收消息不存在，消息来源为" + message.message_from + "消息目标为" + message.message_to)
            self.serves.get(message.message_from).get('send_queue').put(NotFoundMessage(
                message.message_id,
                message.CORE_CONTEXT_MESSAGE,
                message.message_from))

    def deal_base_context_exception(self):
        times = 3
        while times > 0:
            self.logger.info("正在重启基础服务")
            self.serves[ServerConstant.BASE_CONTEXT_NAME]['serve'].terminate()
            recv_queue = Queue(SERVE_QUEUE_SIZE)
            send_queue = Queue(SERVE_QUEUE_SIZE)
            self.serves[ServerConstant.BASE_CONTEXT_NAME]['serve'] = App.BaseContext(device_id=ServerConstant.DEVICE_ID,
                                                                                     send_queue=recv_queue,
                                                                                     recv_queue=send_queue)
            self.serves[ServerConstant.BASE_CONTEXT_NAME] = {
                "serve": self.serves[ServerConstant.BASE_CONTEXT_NAME]['serve'],
                "send_queue": send_queue,
                "recv_queue": recv_queue
            }
            self.serves[ServerConstant.BASE_CONTEXT_NAME]['serve'].start()
            if self.serves[ServerConstant.BASE_CONTEXT_NAME]['serve'].is_alive():
                self.logger.info("基础服务重启成功")
                if time.time() - self.last_start_time < 10:
                    self.logger.error("基础服务重启频繁，退出")
                    sys.exit(-1)
                return
            else:
                self.logger.error("基础服务重启失败")
                times -= 1
            time.sleep(3)
        exit(-1)
