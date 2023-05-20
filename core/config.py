#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/14 16:12
# @Author  : 李帅兵
# @FileName: config.py
# @Software: PyCharm
from abc import ABC, abstractmethod

from .tools import singleton


class ConfigAbstract(ABC):

    def __init__(self, *args, **kwargs):
        self.file_path = kwargs.get("file_path", None)
        self.config = dict()


    @abstractmethod
    def get_config(self):
        pass

    @abstractmethod
    def set_config(self):
        pass

    @abstractmethod
    def get_config_by_key(self):
        pass

    @abstractmethod
    def set_config_by_key(self):
        pass

    @abstractmethod
    def save_config(self):
        pass

    @abstractmethod
    def reload_config(self):
        pass


@singleton
class Core(ConfigAbstract):
    def get_config(self):
        pass

    def set_config(self):
        pass

    def get_config_by_key(self):
        pass

    def set_config_by_key(self):
        pass

    def save_config(self):
        pass

    def reload_config(self):
        pass


@singleton
class BaseContext(ConfigAbstract):
    def get_config(self):
        pass

    def set_config(self):
        pass

    def get_config_by_key(self):
        pass

    def set_config_by_key(self):
        pass

    def save_config(self):
        pass

    def reload_config(self):
        pass


@singleton
class EdgeComputing(ConfigAbstract):
    def get_config(self):
        pass

    def set_config(self):
        pass

    def get_config_by_key(self):
        pass

    def set_config_by_key(self):
        pass

    def save_config(self):
        pass

    def reload_config(self):
        pass


@singleton
class WebCam(ConfigAbstract):
    def get_config(self):
        pass

    def set_config(self):
        pass

    def get_config_by_key(self):
        pass

    def set_config_by_key(self):
        pass

    def save_config(self):
        pass

    def reload_config(self):
        pass


@singleton
class Gui(ConfigAbstract):
    def get_config(self):
        pass

    def set_config(self):
        pass

    def get_config_by_key(self):
        pass

    def set_config_by_key(self):
        pass

    def save_config(self):
        pass

    def reload_config(self):
        pass
