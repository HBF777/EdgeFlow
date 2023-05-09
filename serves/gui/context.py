#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/4/28 16:50
# @Author  : 李帅兵
# @FileName: context.py
# @Software: PyCharm
import time
from threading import Thread

from core.constant import Message, LAMP_DATA_REDIS_KEY,SENSOR_DATA_REDIS_KEY
from core.tools import RedisHelper
from ..serves import BaseServerAbstract

test_op = [
    Message(message_from=Message.GUI_CONTEXT_MESSAGE,
            message_to=Message.BASE_CONTEXT_MESSAGE,
            message_type=Message.TYPE_REQ_DATA_HARD,
            message_target_obj=Message.ALL_SENSOR),
    Message(message_from=Message.GUI_CONTEXT_MESSAGE,
            message_to=Message.BASE_CONTEXT_MESSAGE,
            message_type=Message.TYPE_REQ_DATA_HARD,
            message_target_obj=Message.ALL_SENSOR),
]


class GuiContext(BaseServerAbstract):
    def __init__(self, *args, **kwargs):
        super(GuiContext, self).__init__(*args, **kwargs)

    def keep_alive(self):
        pass

    def run(self):
        self.init_serve()

    def await_get_message(self):
        pass

    def put_message(self):
        pass

    def init_serve(self):
        RedisHelper()
        Thread(target=self.loop_serve_listen).start()
        Thread(target=self.loop_serve_send_test).start()

    def loop_serve_listen(self):
        while True:
            if not self.recv_queue.empty():
                print(self.recv_queue.get())

    def loop_serve_send_test(self):
        for i in test_op:
            if RedisHelper().is_existsKey(SENSOR_DATA_REDIS_KEY):
                print(RedisHelper().get(SENSOR_DATA_REDIS_KEY))
                continue
            time.sleep(1)
            self.send_queue.put(i)

