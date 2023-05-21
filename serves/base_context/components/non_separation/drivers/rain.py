#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/19/10:59
# @Author  : 周伟帆
# @Project : brilliant_clustering
# @File    : rain
# @Software: PyCharm
import smbus
import RPi.GPIO as GPIO
import time
from .baseDriver import Basedriver


GPIO.setmode(GPIO.BCM)
global is_Work
DO = 22

# 感应板上没有水滴时，DO输出为高电平，数字输出指示灯DO-LED灭 ，打印 * It stops raining *。
# 滴上一滴水，DO输出为低电平，数字输出指示灯DO-LED亮，打印 * It Raining *。
# 刷掉上面的水滴，又恢复到输出高电平状态。

class driver(Basedriver):
    address = 0x48
    bus = smbus.SMBus(1)

    def Init_pins(self):
        pass


    def __init__(self, pins):
        super(driver, self).__init__(pins)

    def read(self, chn):  # channel
        if chn == 0:
            self.bus.write_byte(self.address, 0x40)  # 发送一个控制字节到设备
        if chn == 1:
            self.bus.write_byte(self.address, 0x41)
        if chn == 2:
            self.bus.write_byte(self.address, 0x42)
        if chn == 3:
            self.bus.write_byte(self.address, 0x43)
        self.bus.read_byte(self.address)  # 从设备读取单个字节，而不指定设备寄存器。
        return self.bus.read_byte(self.address)  # 返回某通道输入的模拟值A/D转换后的数字值

    def write(self, val):
        temp = val  # 将字符串值移动到temp
        temp = int(temp)  # 将字符串改为整数类型
        # print temp to see on terminal else comment out
        bus.write_byte_data(self.address, 0x40, temp)

    # 写入字节数据，将数字值转化成模拟值从AOUT输出

    def Init_pins(self):
        pass

    def __init__(self, pins):
        self.Init_pins()

    def setup(self):

        GPIO.setup(DO, GPIO.IN)

    def loop(self):
        if is_Work:
            tmp = GPIO.input(DO)
            # 数字输出DO的值（无雨为1，有雨为0）
            rain_num = 255 - self.read(0)
            return rain_num
            '''
            if tmp == 1:
                print("meiyu")
                return 
            else:
                # print(f'测到的雨滴数字值为:{ADC.read(0)} （值越小，雨量越大）')  # 打印A/D转换后的数字值（从AIN0借口输入的）,范围是0~255,0时LED灯熄灭，255时灯最亮
                print("youyu")
                return ADC.read(0)
                '''

    def Init(self):
        global is_Work
        self.setup()
        is_Work = True

    def Test_run(self):
        self.get_data()

    def RAIN_DESTROY(self):
        global is_Work
        is_Work = False
        time.sleep(1)
        GPIO.cleanup()


    def get_data(self):
        self.Init()
        rain = self.loop()
        data = {'rain': rain, "time": time.time()}
        return data
