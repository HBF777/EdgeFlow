#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/4/28 16:50
# @Author  : 李帅兵
# @FileName: context.py
# @Software: PyCharm
import os.path
import threading
import time
from core.constant import *
from .components.component_proxy import ComponentProxy
from .constant import *
from ..serves import BaseServerAbstract
from core.tools import Logger, ConfigParser, singleton
from .com_proxy import ComProxy, Message

device_id = str()
component_config = None


@singleton
class MessageManager(object):
    class MessagePool(object):
        """
        引入消息池机制，用于处理消息的转发及回复的确认功能
        """
        message_pool = {}

        @staticmethod
        def put_message(message: Message):
            """
            放入内部消息
            :param message:
            :return:
            """
            MessageManager().MessagePool.message_pool[message.message_id] = message

        @staticmethod
        def times_up():
            """
            超时处理
            :return:
            """
            for message in MessageManager.MessagePool.message_pool.items():
                m = message.wait()
                if m:
                    MessageManager.MessagePool.message_pool.pop(m.message_id)
                    MessageManager.MessagePool.message_time_out(m)

        @staticmethod
        def message_time_out(message: Message):
            """
            消息超时
            :return:
            """
            pass

        @staticmethod
        def remove_message(message_id: str):
            """
            移除消息
            :param message_id:
            :return:
            """
            return MessageManager().MessagePool.message_pool.pop(message_id, False)

    class MessageQueue(object):
        def __init__(self):
            self.data = []

        def put(self, message: Message):
            self.data.append(message)

        def wait_get(self) -> Message:
            while len(self.data) == 0:
                time.sleep(0.1)
            return self.data.pop(0)

        def get_timeout_message(self) -> Message:
            pass

    def __init__(self):
        self.mqtt_queue = self.MessageQueue()
        self.serial_queue = self.MessageQueue()
        self.serve_send_queue = None
        self.serve_recv_queue = None

    def init(self, serve_queue_send, serve_queue_recv):
        self.serve_send_queue = serve_queue_send
        self.serve_recv_queue = serve_queue_recv

    def get_message(self):
        pass

    def listen_message_cloud(self):
        while True:
            message = self.mqtt_queue.wait_get()
            threading.Thread(target=self.handle_message, args=(message,)).start()

    def handle_message(self, message: Message):
        """
        处理消息
        步骤如下：
        1、 先解析消息来源
        2、 再解析消息类型
        3、
        :param message:
        :return:
        """
        if message.receiver != message.BASE_CONTEXT_MESSAGE:
            self.serve_send_queue.put(message)
            return
        self.MessagePool().put_message(message)
        req_data_type = REQ_TYPE_MQTT if message.sender == message.BASE_CONTEXT_MESSAGE else REQ_TYPE_LOCAL
        if message.message_type == Message.TYPE_CONTROL:  # 控制消息
            pass
        elif message.message_type == Message.TYPE_REQ_DATA_HARD:  # 请求硬件数据
            message = HardManager().get_data(message, req_data_type)
            self.serve_send_queue.put(message)
        self.MessagePool().remove_message(message.message_id)

    def start(self):
        threading.Thread(target=self.listen_message_cloud).start()
        while True:
            time.sleep(4)


@singleton
class HardManager(object):
    def __init__(self, components_config=None):
        self.component_proxy = None
        self.component_config = components_config

    def init(self):
        # 创建硬件代理
        self.component_proxy = ComponentProxy(self.component_config)

    def get_data(self, message, data_type=REQ_TYPE_LOCAL) -> dict:
        """
        处理硬件消息
        消息返回种类有两种
        一种是返回给云端，要携带topic, data
        一种是返回给其他服务，要返回传感器名称：data形式返回
        :param data_type:
        :param message:
        :return:
        """
        if data_type == REQ_TYPE_MQTT:
            self.component_proxy.get_data_topic(message)
            pass
        elif data_type == REQ_TYPE_LOCAL:
            return self.component_proxy.get_data_names(message)


def init_context() -> bool:
    global component_config
    component_config = ConfigParser.parse_json(file_path=os.path.abspath(COMPONENT_CONFIG_FILE_PATH))
    HardManager(components_config=component_config).init()
    return True


def start_com_proxy():
    com_config = ConfigParser.parse_json(file_path=os.path.abspath(COM_CONFIG_FILE_PATH))
    com_config['mqtt']['sub_topics'] = str(com_config['mqtt']['sub_topics']).format(id=device_id)
    ComProxy(com_config, mqtt_message_queue=MessageManager().mqtt_queue,
             serial_message_queue=MessageManager().serial_queue)
    message_manager_thread = threading.Thread(target=MessageManager().start)
    com_proxy_thread = threading.Thread(target=ComProxy().start)
    com_proxy_thread.start()
    message_manager_thread.start()
    while True:
        time.sleep(1)
        if not com_proxy_thread.is_alive():
            Logger().error("com_proxy_thread is dead")
        if not message_manager_thread.is_alive():
            Logger().error("message_manager_thread is dead")


class BaseContext(BaseServerAbstract):
    def __init__(self, *args, **kwargs):
        super(BaseContext, self).__init__(*args, **kwargs)
        self.keep_alive_thread = None
        self.message_thread = None
        self.com_thread = None
        self.task_manager = None
        self.base_path = None

    def run(self):
        global device_id
        device_id = self.device_id
        self.base_path = os.path.abspath(".")
        Logger(filename=LOG_FILE_PATH, level="debug")
        Logger().info("BaseContext init-ing")
        # 初始化基础环境 启动流程 初始化检查硬件 -> 初始化通讯服务 -> 初始化消息服务 -> 初始化心跳服务
        init_context()
        MessageManager().init(self.send_queue, self.recv_queue)
        # 通讯服务启动
        self.com_thread = threading.Thread(target=start_com_proxy)
        # 消息服务启动
        self.message_thread = threading.Thread(target=self.listen_message)
        # 心跳服务启动
        self.keep_alive_thread = threading.Thread(target=self.keep_alive)
        Logger().info("BaseContext 初始化通讯服务")
        self.com_thread.start()
        Logger().info("BaseContext 初始化消息服务")
        self.message_thread.start()
        Logger().info("BaseContext 初始化心跳服务")
        self.keep_alive_thread.start()
        self.listen_threads()

    def keep_alive(self):
        pass

    def await_get_message(self):
        pass

    def put_message(self):
        pass

    def listen_message(self):
        while True:
            if not self.recv_queue.empty():
                message = self.recv_queue.get()
                MessageManager().handle_message(message)

    def listen_threads(self):
        com_thread_start_time = time.time()
        message_thread_start_time = time.time()
        keep_alive_thread_start_time = time.time()
        while True:
            if not self.com_thread.is_alive():
                if time.time() - com_thread_start_time < 10:
                    exit(-1)
                self.com_thread = threading.Thread(target=start_com_proxy)
                com_thread_start_time = time.time()
            if not self.message_thread.is_alive():
                if time.time() - message_thread_start_time < 10:
                    exit(-1)
                self.message_thread.start()
            if not self.keep_alive_thread.is_alive():
                if time.time() - keep_alive_thread_start_time < 10:
                    exit(-1)
                self.keep_alive_thread.start()
            time.sleep(1)
