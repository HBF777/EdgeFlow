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
    # 路灯消息
    LAMP_MESSAGE = "lamp"
    # 传感器消息
    SENSOR_MESSAGE = "sensor"
    # ALL 传感器
    ALL_SENSOR = "sensor_all"
    # ALL 路灯
    ALL_LAMP = "lamp_all"
    # 服务消息类型
    TYPE_DATA_HARD = 'data'
    TYPE_CONTROL = 'control'
    TYPE_NOTICE_NOT_SERVE = "NOT_SERVE"
    TYPE_REQ_DATA_HARD = "req_data_hard"
    TYPE_REQ_DATA_ = "req_data_"
    # 服务指令内容
    MESSAGE_OP_LAMP = 'lamp'
    MESSAGE_OP_SENSOR = 'sensor'

    # 服务消息内容

    def __init__(self, *args, **kwargs):
        if kwargs.get('message_id', None) is None:
            self.message_id = str(uuid.uuid1())
        else:
            self.message_id = kwargs.get("message_id")
        self.message_type = kwargs.get('message_type')
        self.message_from = kwargs.get('message_from')
        self.message_to = kwargs.get('message_to')
        self.message_target_obj = kwargs.get('message_target_obj')
        self.message_op = kwargs.get('message_op')
        self.message_data = kwargs.get('message_data')
        self.message_topic = kwargs.get('message_topic')

    @property
    def topic(self):
        return self.message_topic

    @property
    def receiver(self):
        return self.message_to

    @property
    def sender(self):
        return self.message_from

    @property
    def type(self):
        return self.message_type

    @property
    def data(self):
        return self.message_data

    @property
    def target_obj(self):
        return self.message_target_obj

    @property
    def id(self):
        return self.message_id

    @property
    def op(self):
        return self.message_op

    @property
    def is_to_core_control_self(self) -> bool:
        if self.message_to == Message.CORE_CONTEXT_MESSAGE:
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
    return Message(message_id=message_id, message_type=Message.TYPE_NOTICE_NOT_SERVE,
                   message_from=message_form, message_to=message_to)


def DataMessage(message_data, message_id=None, message_from=None, message_to=None, message_topic=None,
                message: Message = None, ) -> Message:
    if message:
        return Message(message_id=message.message_id,
                       message_type=Message.MESSAGE_TYPE_DATA,
                       message_from=message.receiver,
                       message_to=message.sender,
                       message_data=message_data,
                       message_topic=message_topic)
    return Message(message_type=Message.MESSAGE_TYPE_DATA,
                   message_from=message_from,
                   message_to=message_to,
                   message_data=message_data)


def TestMessage() -> Message:
    return Message(message_from=Message.BASE_CONTEXT_MESSAGE,
                   message_to=Message.GUI_CONTEXT_MESSAGE,
                   message_op=Message.MESSAGE_TYPE_DATA,
                   message_data="ssss")
