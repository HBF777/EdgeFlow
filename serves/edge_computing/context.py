#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/4/28 16:50
# @Author  : 李帅兵
# @FileName: context.py
# @Software: PyCharm
import queue

from .algorithms.algorithms_factory import algo_factory
from ..serves import BaseServerAbstract
from threading import Thread


class EdgeComputingContext(BaseServerAbstract):
    def run(self):
        self.algo_factory = algo_factory()
        self.recv_factory_queue = queue.Queue()
        self.send_factory_queue = queue.Queue()
        keep_alive_thread = Thread(target=self.keep_alive).start()
        message_manager = Thread(target=self.message_handler).start()
        while True:
            algo = self.algo_factory.get_algo()
            algo.execute()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.send_factory_queue = None
        self.recv_factory_queue = None
        self.algo_factory = None

    def message_handler(self):
        pass

    def keep_alive(self):
        while True:
            pass

    def await_get_message(self):
        pass

    def put_message(self):
        pass
