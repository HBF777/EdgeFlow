#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/4/28 16:46
# @Author  : 李帅兵
# @FileName: constant.py
# @Software: PyCharm
import uuid

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


class Message:
    # 基础服务消息
    BASE_CONTEXT_MESSAGE = ServerConstant.BASE_CONTEXT_NAME
    # GUI服务消息
    GUI_CONTEXT_MESSAGE = ServerConstant.GUI_CONTEXT_NAME
    # 摄像头服务消息
    WEBCAM_CONTEXT_MESSAGE = ServerConstant.WEBCAM_CONTEXT_NAME
    # 边缘计算服务消息
    EDGE_COMPUTING_CONTEXT_MESSAGE = ServerConstant.EDGE_COMPUTING_CONTEXT_NAME
    # APP 控制消息
    CORE_CONTEXT_MESSAGE = "app_core"
    # 云端消息
    CLOUD_CONTEXT_MESSAGE = "cloud"
    # 硬件消息
    HARDWARE_CONTEXT_MESSAGE = "hardware"
    # 服务消息类型
    MESSAGE_TYPE_DATA = 'data'
    MESSAGE_TYPE_OP = 'op'
    MESSAGE_TYPE_NOTICE_NOT_SERVE = "NOT_SERVE"
    # 服务指令内容
    MESSAGE_OP_LAMP = 'lamp'
    # 服务消息内容

    def __init__(self, *args, **kwargs):
        self.message_id = kwargs.get("message_id") if kwargs.get('message_id') else uuid.uuid4()
        self.message_type = kwargs.get('message_type')
        self.message_from = kwargs.get('message_from')
        self.message_to = kwargs.get('message_to')
        self.message_op = kwargs.get('message_op')
        self.message_data = kwargs.get('message_data')

    def is_op(self) -> bool:
        if self.message_type == Message.MESSAGE_TYPE_OP:
            return True
        return False

    def __str__(self):
        return str({
            "id": self.message_id,
            "type": self.message_type,
            "from": self.message_from,
            "to": self.message_to,
            "op": self.message_op,
            "data": self.message_data
        })


def NotFoundMessage(message_id, message_form, message_to) -> Message:
    return Message(message_id=message_id, message_type=Message.MESSAGE_TYPE_NOTICE_NOT_SERVE,
                   message_from=message_form, message_to=message_to)


def DataMessage(message: Message) -> Message:
    return message


def TestMessage() -> Message:
    return Message(message_from=Message.BASE_CONTEXT_MESSAGE,
                   message_to=Message.GUI_CONTEXT_MESSAGE,
                   message_op=Message.MESSAGE_TYPE_DATA,
                   message_data="ssss")
