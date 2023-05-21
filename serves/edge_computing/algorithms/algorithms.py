#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/21 18:58
# @Author  : 李帅兵
# @FileName: algorithms.py
# @Software: PyCharm
# 导入所需的传感器模块和时间模块
from serves.edge_computing.algorithms.algorithms_factory import Algorithm
from ..constant import RADAR, CAMERA, LIDAR
from time import time
from datetime import datetime


class MainRoadAlgorithm(Algorithm):
    class power_saving_mode:
        is_active = False

        @staticmethod
        def activate():
            if MainRoadAlgorithm.power_saving_mode.is_active:
                return
            MainRoadAlgorithm.power_saving_mode.is_active = True
            # 控制路灯组进入省电模式
            MainRoadAlgorithm.set_lightness(20)

    class normal_mode:
        @staticmethod
        def activate():
            pass

    def execute(self):
        # 读取雷达距离传感器数据
        distance = self.get_distance(RADAR)

        # 读取环境亮度传感器数据
        brightness = self.get_brightness()

        # 获取当前时间
        current_time = datetime.now().strftime('%H:%M')

        if distance <= 10:
            if brightness <= 50 or ('18:00' <= current_time <= '06:00'):
                # 如果距离小于等于10米且亮度低于等于50，或者在晚上18:00到早上6:00之间，执行省电模式
                self.power_saving_mode.activate()

                # 控制相邻的两个路灯组进入省电模式
                # neighboring_lamp_id_1 = current_lamp_id - 1
                # neighboring_lamp_id_2 = current_lamp_id + 1
                # cloud_controller.set_power_saving_mode(neighboring_lamp_id_1)
                # cloud_controller.set_power_saving_mode(neighboring_lamp_id_2)
            else:
                # 否则，执行正常模式
                self.normal_mode.activate()

                # 控制相邻的两个路灯组进入正常模式
                # neighboring_lamp_id_1 = current_lamp_id - 1
                # neighboring_lamp_id_2 = current_lamp_id + 1
                # cloud_controller.set_normal_mode(neighboring_lamp_id_1)
                # cloud_controller.set_normal_mode(neighboring_lamp_id_2)


# 导入所需的传感器模块和时间模块

class SideRoadAlgorithm(Algorithm):
    def execute(self):
        # 读取雷达距离传感器数据
        distance = self.get_distance(RADAR)

        # 读取环境亮度传感器数据
        brightness = self.get_brightness()

        # 获取当前时间
        current_time = datetime.now().strftime('%H:%M')

        if distance <= 10:
            if brightness <= 50 or ('18:00' <= current_time <= '06:00'):
                # 如果距离小于等于10米且亮度低于等于50，或者在晚上18:00到早上6:00之间，执行省电模式
                self.power_saving_mode.activate()

                # 控制相邻的两个路灯组进入省电模式
                # neighboring_lamp_id_1 = current_lamp_id - 1
                # neighboring_lamp_id_2 = current_lamp_id + 1
                # cloud_controller.set_power_saving_mode(neighboring_lamp_id_1)
                # cloud_controller.set_power_saving_mode(neighboring_lamp_id_2)
            else:
                # 否则，执行正常模式
                self.normal_mode.activate()

