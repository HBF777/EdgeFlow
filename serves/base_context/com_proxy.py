#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/3 20:56
# @Author  : 李帅兵
# @FileName: com_proxy.py
# @Software: PyCharm
import abc

from paho import mqtt

from .constant import *


class CommunicationClient(metaclass=abc.ABCMeta):
    def __init__(self, config):
        self.logger = config['logger']
        pass

    @abc.abstractmethod
    def connect(self):
        pass

    @abc.abstractmethod
    def send_message(self):
        pass

    @abc.abstractmethod
    def recv_message(self):
        pass

    @abc.abstractmethod
    def disconnect(self):
        pass


class MqttClient(CommunicationClient):
    def recv_message(self):
        self.client.subscribe(self.sub_topics)
        self.client.loop_forever()

    def disconnect(self):
        pass

    def __init__(self, conf):
        """
        profile: {
                  "host_ip": "",
                  "host_port": "",
                  "account": "",
                  "passwd": "",
                  "keepalive": "",
                  ""
              }
        :param conf:
        """
        super().__init__(conf)
        self.target_host = conf['host']
        self.target_port = conf['port']
        self.account = conf['account']
        self.password = conf['passwd']
        self.message_queue = conf['message_queue']
        self.client = mqtt.Client()
        self.client.username_pw_set(self.account, self.password)
        self.client.on_message = self.__on_message
        self.client.reconnect_delay_set(min_delay=1, max_delay=2000)
        self.sub_topics = conf['sub_topics']

    def __on_message(self, client, userdata, msg):
        """
        :param client:
        :param userdata:
        :param msg:
        :return:
        """
        # print("收到消息: 主题: %s,消息: %s" % (msg.topic, msg.payload.decode('utf-8')))
        self.logger.logger.info("收到消息: 主题: %s,消息: %s" % (msg.topic, msg.payload.decode('utf-8')))
        message_type = parse_msg_type_by_topic(msg.topic)
        message = Message(message_type=message_type, data=msg.payload.decode('utf-8'))
        self.message_queue.put(message)
        # self.message_queue.put((CONTEXT_SENSOR_MESSAGE, orin_message))

    def connect(self):
        try:
            self.client.connect(host=self.target_host, port=self.target_port, keepalive=60)
            self.logger.logger.info("成功连接MQTT服务器")
        except Exception as e:
            raise e

    def subscribe(self):
        self.client.subscribe(self.sub_topics)

    def send_message(self):
        pass


class SerialClient(CommunicationClient):
    def connect(self):
        pass

    def send_message(self):
        pass

    def recv_message(self):
        pass

    def disconnect(self):
        pass


class Message:
    def __init__(self, data: dict, message_type: str):
        self.data = data
        self.message_type = message_type
        self.channel = None


class ComProxy:
    class ComProxyMessageQueue:
        def __init__(self):
            self.lamp_message = []
            self.serve_message = []
            self.sensor_message = []
            self.data = {
                ComProxy_MESSAGE_LAMP: self.lamp_message,
                ComProxy_MESSAGE_SERVE: self.serve_message,
                ComProxy_MESSAGE_SENSOR: self.sensor_message
            }

        def put(self, message: Message):
            if message.message_type == ComProxy_MESSAGE_LAMP or message.message_type == ComProxy_MESSAGE_SENSOR:
                message.channel = BASE_MESSAGE_CHANNEL
                self.data[message.message_type].append(message)
            else:
                message.channel = SERVE_MESSAGE_CHANNEL
                self.data[ComProxy_MESSAGE_SERVE].append(message)

        def empty(self):
            if len(self) < 1:
                return True
            return False

        def empty_base(self):
            if len(self.lamp_message) == 0 and len(self.serve_message) == 0:
                return True
            return False

        def empty_serve(self):
            if len(self.serve_message) == 0:
                return True
            return False

        def get(self):
            if len(self.serve_message) > 0:
                return self.serve_message.pop(0)
            elif len(self.lamp_message) > 0:
                return self.lamp_message.pop(0)
            elif len(self.serve_message) > 0:
                return self.serve_message.pop(0)
            raise Exception("base context message queue is empty")

        def get_base_context(self):
            if len(self.lamp_message) > 0:
                return self.lamp_message.pop(0)
            elif len(self.serve_message) > 0:
                return self.serve_message.pop(0)
            raise Exception("base context message queue is empty")

        def get_serve_message(self):
            if len(self.serve_message) > 0:
                return self.serve_message.pop(0)
            raise Exception("serve message queue is empty")

        def __len__(self):
            return len(self.lamp_message) + len(self.serve_message) + len(self.sensor_message)

    pass


def parse_msg_type_by_topic(topic):
    """
    解析MQTT Topic并返回消息类型。
    :param topic: MQTT Topic，格式为/serve/{device_id}/{serve_type}/#
    :return: 消息类型字符串
    """
    parts = topic.split("/")
    if len(parts) < 4 or parts[0] != "server":
        raise ValueError("Invalid MQTT topic format.")
    serve_type = parts[2]
    if serve_type == "base_context":
        if parts[3] == "lamp":
            return ComProxy_MESSAGE_LAMP
        return ComProxy_MESSAGE_SENSOR
    elif serve_type == "gui":
        return ComProxy_MESSAGE_GUI
    elif serve_type == "webcam":
        return ComProxy_MESSAGE_WEBCAM
    elif serve_type == "edge_computing":
        return ComProxy_MESSAGE_EDGE_COMPUTING
    raise ValueError("Invalid MQTT topic format.")
