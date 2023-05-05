#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/4/28 17:07
# @Author  : 李帅兵
# @FileName: tools.py
# @Software: PyCharm

import redis
import logging
from logging import handlers
import json
import xml.etree.ElementTree as ET
import yaml


class RedisHelper:
    def __init__(self, host="121.37.108.178", password="huba20020402", port=6739):
        # 连接redis
        self.__redis = redis.StrictRedis(host=host, password=password, port=port)

    # 设置key-value
    def set(self, key, value):
        self.__redis.set(key, value)

    # 获取key-value
    def get(self, key):
        return self.__redis.get(key).decode()

    # 判断key是否存在
    def is_existsKey(self, key):
        # 返回1存在，0不存在
        return self.__redis.exists(key)

    # 添加集合操作
    def add_set(self, key, value):
        # 集合中存在该元素则返回0,不存在则添加进集合中，并返回1
        # 如果key不存在，则创建key集合，并添加元素进去,返回1
        return self.__redis.sadd(key, value)

    # 判断value是否在key集合中
    def is_Inset(self, key, value):
        '''判断value是否在key集合中，返回布尔值'''
        return self.__redis.sismember(key, value)

    # 关闭连接
    def close(self):
        self.__redis.close()


class Logger(object):
    # 日志级别关系映射
    level_relations = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL
    }

    def __init__(self, filename="./log/test.log", level="debug", when="D", backupCount=3,
                 fmt="%(asctime)s - %(pathname)s[line:%(lineno)d] - %"
                     "(levelname)s: %(message)s"):
        # 设置日志输出格式
        format_str = logging.Formatter(fmt)
        # 设置日志在控制台输出
        streamHandler = logging.StreamHandler()
        # 设置控制台中输出日志格式
        streamHandler.setFormatter(format_str)
        # 设置日志输出到文件（指定间隔时间自动生成文件的处理器  --按日生成）
        # filename：日志文件名，interval：时间间隔，when：间隔的时间单位， backupCount：备份文件个数，若超过这个数就会自动删除
        fileHandler = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backupCount,
                                                        encoding="utf-8")
        # 设置日志文件中的输出格式
        fileHandler.setFormatter(format_str)
        # 设置日志输出文件
        self.logger = logging.getLogger(filename)
        # 设置日志级别
        self.logger.setLevel(self.level_relations.get(level))
        # 将输出对象添加到logger中
        self.logger.addHandler(streamHandler)
        self.logger.addHandler(fileHandler)


class ConfigParser:

    @staticmethod
    def parse(file_path, file_format="json", data_format="dict"):
        if file_format == "json":
            return ConfigParser.parse_json(file_path, data_format)
        elif file_format == "xml":
            return ConfigParser.parse_xml(file_path, data_format)
        elif file_format == "yaml":
            return ConfigParser.parse_yaml(file_path, data_format)
        else:
            raise ValueError("Unsupported format")

    # 解析Json配置文件
    @staticmethod
    def parse_json(file_path, data_format="dict"):
        if data_format == "dict":
            with open(file_path, "r", encoding="utf8") as f:
                return json.load(f)
        elif data_format == "str":
            with open(file_path, "r") as f:
                return json.dumps(f)
        elif data_format == "obj":
            with open(file_path, "r") as f:
                return json.load(f)
        elif data_format == "list":
            with open(file_path, "r") as f:
                return list(json.load(f))

    @staticmethod
    def parse_yaml(file_path, data_format="dict"):
        if data_format == "dict":
            with open(file_path, "r") as f:
                return yaml.safe_load(f)
        elif data_format == "str":
            with open(file_path, "r") as f:
                return yaml.dump(f)
        elif data_format == "obj":
            with open(file_path, "r") as f:
                return yaml.safe_load(f)
        elif data_format == "list":
            with open(file_path, "r") as f:
                return list(yaml.safe_load(f))

    @staticmethod
    def new_config(file_path, data, file_format="json"):
        # 根据文件不同类型选择不同的解析方式
        if file_format == "json":
            return ConfigParser.new_json(file_path, data)
        elif file_format == "xml":
            return ConfigParser.new_xml(file_path, data)
        elif file_format == "yaml":
            return ConfigParser.new_yaml(file_path, data)

    @staticmethod
    def new_json(file_path, data):
        data_format = type(data)
        if data_format == dict:
            with open(file_path, "w") as f:
                json.dump(data, f)
        elif data_format == str:
            with open(file_path, "w") as f:
                json.loads(data, f)
        elif data_format == list:
            with open(file_path, "w") as f:
                data_dict = {}
                for i in range(len(data)):
                    data_dict[i] = data[i]
                json.dump(data_dict, f)
        else:
            raise ValueError("Unsupported data format")

    @staticmethod
    def append_config(file_path, data, file_format="json"):
        # 根据文件不同类型选择不同的解析方式
        if file_format == "json":
            return ConfigParser.append_json(file_path, data)
        elif file_format == "xml":
            return ConfigParser.append_xml(file_path, data)
        elif file_format == "yaml":
            return ConfigParser.append_yaml(file_path, data)

    @staticmethod
    def append_json(file_path, data):
        data_format = type(data)
        if data_format == dict:
            # original = ConfigParser.parse_json(file_path, "dict")
            # original = original + data
            with open(file_path, "a") as f:
                json.dump(data, f)
        elif data_format == str:
            with open(file_path, "a") as f:
                json.loads(data, f)
        elif data_format == list:
            with open(file_path, "a") as f:
                data_dict = {}
                for i in range(len(data)):
                    data_dict[i] = data[i]
                json.dump(data_dict, f)
        else:
            raise ValueError("Unsupported data format")
