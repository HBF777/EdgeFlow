#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :event_handler.py
# @Time      :2023/5/6 14:21
# @Author    :李帅兵
import queue
import time

event_queue = queue.Queue()
TaskList = []


class Task:
    def __init__(self, name,task, *args):
        self.name = name
        self.task = task
        self.state = None

    def exam_state(self):
        if self.task.get_state() != self.state:
            self.state = self.task.get_state()
            event = (self.name, self.state)
            event_queue.put(event)

    def get_state(self):
        return 1


class EventHandler:
    def __call__(self, event):
        print(f"Event {event} happened. Taking corresponding actions...")

    @staticmethod
    def mqtt_event_handler(event):
        print(f"Event {event} happened. Taking corresponding actions...")

    @staticmethod
    def hard_event_handler(event):
        print(f"Event {event} happened. Taking corresponding actions...")


def event_loop():
    while True:
        if event_queue.empty():
            continue
        event = event_queue.get()
        thread_name, state = event
        print(f"Thread {thread_name} state changed to {state}.")
        EventHandler()(event)
