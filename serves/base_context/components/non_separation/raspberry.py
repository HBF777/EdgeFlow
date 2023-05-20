#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :raspberry.py
# @Time      :2023/5/5 10:12
# @Author    :李帅兵
from ..abc_component import Lamp as LampBase
from ..abc_component import Sensor as SensorBase


class Lamp(LampBase):
    def __init__(self, config):
        super().__init__(config)

    def init(self):
        self.logger.info("Lamp" + self.get_name() + " init")

    def set_light(self, light):
        self.logger.info("Lamp" + self.get_name() + " set_light:" + light)
        pass

    def get_data(self):
        data_frame = self.config['data_format']
        data_frame['brightness'] = 20
        return data_frame


class TempHumSensor(SensorBase):
    def __init__(self, config):
        super().__init__(config)

    def init(self):
        self.logger.info("TempHumSensor" + self.get_name() + " init")

    def get_data(self):
        data_frame = self.config['data_format']
        data_frame['temperature'] = 20
        data_frame['humidity'] = 30
        return data_frame


class LightSensor(SensorBase):
    def __init__(self, config):
        super().__init__(config)

    def init(self):
        pass

    def get_data(self):
        data_frame = self.config['data_format']
        data_frame['brightness'] = 20
        return data_frame

# 光敏传感器
# 外部
class Brightness_Ext(SensorBase):
    def __init__(self, config):
        super().__init__(config)

    def init(self):
        pass

    def get_data(self):
        data_frame = self.config['data_format']
        data_frame['brightness'] = 20
        return data_frame

# 光敏
# 内部
class Brightness_In(SensorBase):
    def __init__(self, config):
        super().__init__(config)

    def init(self):
        pass

    def get_data(self):
        data_frame = self.config['data_format']
        data_frame['brightness'] = 20
        return data_frame

# 二氧化碳
class Co2(SensorBase):
    def __init__(self, config):
        super().__init__(config)

    def init(self):
        pass

    def get_data(self):
        data_frame = self.config['data_format']
        data_frame['brightness'] = 20
        return data_frame


# gps

# 温湿度

# 雨滴



# 光敏传感器
# 外部
class Brightness_Ext(SensorBase):
    def __init__(self, config):
        super().__init__(config)

    def init(self):
        pass

    def get_data(self):
        data_frame = self.config['data_format']
        data_frame['brightness'] = 20
        return data_frame

# 光敏
# 内部
class Brightness_In(SensorBase):
    def __init__(self, config):
        super().__init__(config)

    def init(self):
        pass

    def get_data(self):
        data_frame = self.config['data_format']
        data_frame['brightness'] = 20
        return data_frame

# 二氧化碳
class Co2(SensorBase):
    def __init__(self, config):
        super().__init__(config)

    def init(self):
        pass

    def get_data(self):
        data_frame = self.config['data_format']
        data_frame['brightness'] = 20
        return data_frame


# gps

# 温湿度

# 雨滴


