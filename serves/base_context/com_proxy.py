#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/3 20:56
# @Author  : 李帅兵
# @FileName: com_proxy.py
# @Software: PyCharm
import abc
import asyncio
import threading
import time
import uuid

from paho.mqtt import client as mqtt
from core.constant import Message
from core.tools import Logger, singleton
from .constant import *


class CommunicationClient(metaclass=abc.ABCMeta):
    def __init__(self, message_queue=None):
        self.message_queue = message_queue
        pass

    @abc.abstractmethod
    def connect(self):
        pass

    @abc.abstractmethod
    def send_message(self, message):
        pass

    @abc.abstractmethod
    def recv_message(self):
        pass

    @abc.abstractmethod
    def disconnect(self):
        pass


class MqttClient(CommunicationClient):

    def disconnect(self):
        pass

    def __init__(self, config, message_queue=None):
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
        super().__init__( message_queue)
        self.target_host = config['host']
        self.target_port = config['port']
        self.account = config['account']
        self.password = config['passwd']
        self.client = mqtt.Client(client_id=config['client_id'], clean_session=False)
        self.client.username_pw_set(self.account, self.password)
        self.client.on_message = self.__on_message
        self.client.reconnect_delay_set(min_delay=1, max_delay=2000)
        self.sub_topics = config['sub_topics']

    def __on_message(self, client, userdata, msg):
        """
        :param client:
        :param userdata:
        :param msg:
        :return:
        """
        # print("收到消息: 主题: %s,消息: %s" % (msg.topic, msg.payload.decode('utf-8')))
        Logger().info("收到消息: 主题: %s,消息: %s" % (msg.topic, msg.payload.decode('utf-8')))
        try:
            message = self.parse_msg_type_by_topic(msg.topic)
            message.message_data = msg.payload.decode('utf-8')
            self.message_queue.put(message)
        except ValueError:
            Logger().error("消息格式错误: %s" % msg.payload.decode('utf-8'))
        except Exception as e:
            Logger().error("消息接收错误: %s" % e)
        # self.message_queue.put((CONTEXT_SENSOR_MESSAGE, orin_message))

    def connect(self):
        try:
            self.client.connect(host=self.target_host, port=self.target_port, keepalive=60)
            Logger().info("成功连接MQTT服务器")
        except Exception as e:
            raise e

    def subscribe(self):
        self.client.subscribe(self.sub_topics)

    def recv_message(self):
        self.client.subscribe(self.sub_topics)
        self.client.loop_forever()

    def send_message(self, message: Message):
        self.client.publish(message.topic, str(message.data))

    def reconnect(self):
        self.client.reconnect()

    @property
    def state(self):
        return self.client._state

    @staticmethod
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
        message = Message()
        message.message_from = Message.CLOUD_CONTEXT_MESSAGE
        if serve_type == "base_context":
            message.message_type = Message.TYPE_REQ_DATA_HARD
            message.message_to = Message.BASE_CONTEXT_MESSAGE
            message.message_op = Message.MESSAGE_OP_SENSOR
            if parts[3] == "lamp":
                message.message_type = Message.TYPE_CONTROL
                message.message_op = Message.MESSAGE_OP_LAMP
            message.message_target_obj = parts[4]
            return message
        elif serve_type == "gui":
            message.message_type = Message.TYPE_CONTROL
            message.message_to = Message.GUI_CONTEXT_MESSAGE
            message.message_op = parts[3]
            return message
        elif serve_type == "webcam":
            message.message_type = Message.TYPE_CONTROL
            message.message_to = Message.WEBCAM_CONTEXT_MESSAGE
            message.message_op = parts[3]
            return message
        elif serve_type == "edge_computing":
            message.message_type = Message.TYPE_CONTROL
            message.message_to = Message.EDGE_COMPUTING_CONTEXT_MESSAGE
            message.message_op = parts[3]
            return message
        raise ValueError("Invalid MQTT topic format.")


class SerialClient(CommunicationClient):
    def __init__(self, config, logger=None, message_queue=None):
        super(SerialClient, self).__init__(logger, message_queue)
        pass

    def connect(self):
        pass

    def send_message(self, message):
        pass

    def recv_message(self):
        pass

    def disconnect(self):
        pass


@singleton
class ComProxy:
    def __init__(self, config, mqtt_message_queue, serial_message_queue):
        self.mqtt_client = MqttClient(config['mqtt'],  mqtt_message_queue)
        self.serial_client = SerialClient(config['serial'],  serial_message_queue)

    def start(self):
        Logger().info("启动通信代理")
        self.mqtt_client.connect()
        threading.Thread(target=self.mqtt_client.recv_message).start()
        self.serial_client.connect()
        threading.Thread(target=self.serial_client.recv_message).start()
        self.exam_com_state()

    def get_message_wait(self):
        pass

    def exam_com_state(self):
        while True:
            if self.mqtt_client.state == NOT_CONNECT:
                self.mqtt_client.reconnect()
            time.sleep(1)

    def send_message(self, message: Message):
        self.mqtt_client.send_message(message)
    # class ComProxyMessageQueue:
    #     def __init__(self):
    #         self.lamp_message = []
    #         self.serve_message = []
    #         self.sensor_message = []
    #         self.data = {
    #             ComProxy_MESSAGE_LAMP: self.lamp_message,
    #             ComProxy_MESSAGE_SERVE: self.serve_message,
    #             ComProxy_MESSAGE_SENSOR: self.sensor_message
    #         }
    #
    #     def put(self, message: Message):
    #         if message.message_type == ComProxy_MESSAGE_LAMP or message.message_type == ComProxy_MESSAGE_SENSOR:
    #             message.channel = BASE_MESSAGE_CHANNEL
    #             self.data[message.message_type].append(message)
    #         else:
    #             message.channel = SERVE_MESSAGE_CHANNEL
    #             self.data[ComProxy_MESSAGE_SERVE].append(message)
    #
    #     def empty(self):
    #         if len(self) < 1:
    #             return True
    #         return False
    #
    #     def empty_base(self):
    #         if len(self.lamp_message) == 0 and len(self.serve_message) == 0:
    #             return True
    #         return False
    #
    #     def empty_serve(self):
    #         if len(self.serve_message) == 0:
    #             return True
    #         return False
    #
    #     def get(self):
    #         if len(self.serve_message) > 0:
    #             return self.serve_message.pop(0)
    #         elif len(self.lamp_message) > 0:
    #             return self.lamp_message.pop(0)
    #         elif len(self.serve_message) > 0:
    #             return self.serve_message.pop(0)
    #         raise Exception("base context message queue is empty")
    #
    #     def get_base_context(self):
    #         if len(self.lamp_message) > 0:
    #             return self.lamp_message.pop(0)
    #         elif len(self.serve_message) > 0:
    #             return self.serve_message.pop(0)
    #         raise Exception("base context message queue is empty")
    #
    #     def get_serve_message(self):
    #         if len(self.serve_message) > 0:
    #             return self.serve_message.pop(0)
    #         raise Exception("serve message queue is empty")
    #
    #     def __len__(self):
    #         return len(self.lamp_message) + len(self.serve_message) + len(self.sensor_message)
