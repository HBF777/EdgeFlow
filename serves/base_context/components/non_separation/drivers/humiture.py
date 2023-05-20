#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/13 18:41
# @Author  : 李帅兵
# @Project : Brilliant_Lamp_clustering
# @File    : humiture.py
# @Software: PyCharm
import abc
import time
import smbus2
AHT10_ADDRESS = 0x38  # AHT10 i2c地址
AHT_TEMPERATURE_CONST = 200  # 温度常量
AHT_TEMPERATURE_OFFSET = 50  # 温度偏移
CMD_INITIALIZE = [0xE1, 0x08, 0x00]  # 初始化命令
CMD_RESET = 0xBA  # 复位命令
CMD_MEASURE = [0xAC, 0x33, 0x00]  # 测量命令
global i2c
global aht10
from .baseDriver import Basedriver


class driver(Basedriver):
    class AHT10:
        def __init__(self, i2c):
            if i2c is None:
                raise ValueError('I2C object required.')
            self.i2c = i2c
            self.address = AHT10_ADDRESS
            self.aht10_init()
            self.readings_raw = []
            self.results_parsed = [0, 0]

        # 初始化AHT10
        def aht10_init(self):
            self.aht10_reset()
            self.i2c.write_i2c_block_data(self.address, 0x70, CMD_INITIALIZE)

        # 复位
        def aht10_reset(self):
            self.i2c.write_byte_data(self.address, 0x70, CMD_RESET)
            time.sleep(0.1)

        # 读数据
        def read_raw(self):
            self.i2c.write_i2c_block_data(self.address, 0x70, CMD_MEASURE)
            time.sleep(0.075)
            self.readings_raw = self.i2c.read_i2c_block_data(AHT10_ADDRESS, 0x71, 6)
            self.results_parsed[0] = self.readings_raw[1] << 12 | self.readings_raw[2] << 4 | self.readings_raw[3] >> 4
            self.results_parsed[1] = (self.readings_raw[3] & 0x0F) << 16 | self.readings_raw[4] << 8 | \
                                     self.readings_raw[5]

        # 湿度
        @property
        def humidity(self):
            self.read_raw()
            return (self.results_parsed[0] / 0x100000) * 100
            # 温度

        @property
        def temperature(self):
            self.read_raw()
            return (self.results_parsed[1] / 0x100000) * AHT_TEMPERATURE_CONST - AHT_TEMPERATURE_OFFSET

    def Init_pins(self):
        """
        初始化管脚
        :return:
        """
        global i2c
        global aht10
        i2c = smbus2.SMBus(1)
        aht10 = self.AHT10(i2c)

    def __init__(self, pins):
        super(driver, self).__init__(pins)

    def get_data(self):
        """
        返回时要注意需要返回字典格式的数据
        如
        {
        "humidity": ""
        "temperature": ""
        }
        :return:
        """
        test_data = {"humidity": round(eval(str(aht10.temperature)),2),"temperature": round(eval(str(aht10.humidity)),2),"time": time.time()}
        return test_data
"""

                    data = {'longitude': str(mglng), 'latitude': str(mglat), "time": time.time()}
"""