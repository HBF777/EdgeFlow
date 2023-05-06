#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/4/28 16:50
# @Author  : 李帅兵
# @FileName: context.py
# @Software: PyCharm
import time
from threading import Thread

from core.constant import Message
from ..serves import BaseServerAbstract

test_op = [
    Message(message_from=Message.GUI_CONTEXT_MESSAGE,
            message_to=Message.BASE_CONTEXT_MESSAGE,
            message_type=Message.TYPE_REQ_DATA_HARD,
            message_obj=Message.ALL_SENSOR),
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
        Thread(target=self.loop_serve_listen).start()
        Thread(target=self.loop_serve_send_test).start()

    def loop_serve_listen(self):
        while True:
            if not self.recv_queue.empty():
                print(self.recv_queue.get())

    def loop_serve_send_test(self):
        for i in test_op:
            time.sleep(1)
            self.send_queue.put(i)
