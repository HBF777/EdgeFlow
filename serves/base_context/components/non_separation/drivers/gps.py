# -*- codeing = utf-8 -*-
# @Time : 2022/10/14 14:55
# @Autor: 李帅兵 202003024036
# @File : gps.py
# @Software：PyCharm
import math
import time
import sys
import re
import pynmea2
import serial
import chardet
from socket import socket
from .baseDriver import Basedriver

global Latitude
global Longitude
global line
global line1
global ser2

x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # Semi-major axis
ee = 0.00669342162296594323  # Eccentricity squared


class driver(Basedriver):

    def Init_pins(self):
        """
                初始化管脚
                :return:
                """
        global ser1
        ser1 = serial.Serial("/dev/ttyUSB0", 9600)

    def __init__(self, pins):
        super(driver, self).__init__(pins)

    @staticmethod
    def _transformlat(longitude, latitude):
        ret = -100.0 + 2.0 * longitude + 3.0 * latitude + 0.2 * latitude * latitude + \
              0.1 * longitude * latitude + 0.2 * math.sqrt(math.fabs(longitude))
        ret += (20.0 * math.sin(6.0 * longitude * pi) + 20.0 *
                math.sin(2.0 * longitude * pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(latitude * pi) + 40.0 *
                math.sin(latitude / 3.0 * pi)) * 2.0 / 3.0
        ret += (160.0 * math.sin(latitude / 12.0 * pi) + 320 *
                math.sin(latitude * pi / 30.0)) * 2.0 / 3.0
        return ret

    @staticmethod
    def _transformlng(longitude, latitude):
        ret = 300.0 + longitude + 2.0 * latitude + 0.1 * longitude * longitude + \
              0.1 * longitude * latitude + 0.1 * math.sqrt(math.fabs(longitude))
        ret += (20.0 * math.sin(6.0 * longitude * pi) + 20.0 *
                math.sin(2.0 * longitude * pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(longitude * pi) + 40.0 *
                math.sin(longitude / 3.0 * pi)) * 2.0 / 3.0
        ret += (150.0 * math.sin(longitude / 12.0 * pi) + 300.0 *
                math.sin(longitude / 30.0 * pi)) * 2.0 / 3.0
        return ret

    def get_data(self):
        while True:
            line = str(ser1.readline(), encoding='utf-8')
            if line.startswith("$GNRMC"):
                global Longitude
                global Latitude
                rmc = pynmea2.parse(line)
                if re.match("^\d+?\.\d+?$", rmc.lat) is not None:
                    # print(rmc)
                    latitude = rmc.latitude
                    longitude = rmc.longitude

                    # Coordinate system transformation
                    dlat = driver._transformlat(longitude - 105.0, latitude - 35.0)
                    dlng = driver._transformlng(longitude - 105.0, latitude - 35.0)
                    radlat = latitude / 180.0 * pi
                    magic = math.sin(radlat)
                    magic = 1 - ee * magic * magic
                    sqrtmagic = math.sqrt(magic)
                    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
                    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
                    mglat = latitude + dlat
                    mglng = longitude + dlng
                    data = {'longitude': str(mglng), 'latitude': str(mglat), "time": time.time()}
                    return data
