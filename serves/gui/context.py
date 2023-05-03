#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/4/28 16:50
# @Author  : 李帅兵
# @FileName: context.py
# @Software: PyCharm
from threading import Thread

from ..serves import BaseServerAbstract


class GuiContext(BaseServerAbstract):
    def __init__(self, *args, **kwargs):
        super(GuiContext, self).__init__(*args,**kwargs)

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

    def loop_serve_listen(self):
        while True:
            if not self.recv_queue.empty():
                print(self.recv_queue.get())

