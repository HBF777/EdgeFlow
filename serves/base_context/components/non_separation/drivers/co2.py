#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/11/19/11:32
# @Author  : 周伟帆
# @Project : brilliant_clustering - 新灯
# @File    : co2
# @Software: PyCharm
from smbus2 import SMBus
from sgp30 import Sgp30
import time
import os.path
import datetime
import schedule
from .baseDriver import Basedriver
# def run_recordData():
#     print(".",end="")
#     print()
#     print(sgp.read_measurements())
#     TimeNow=datetime.datetime.now().strftime('%H:%M')
#     co2Data.append(sgp.read_measurements()[0][0])
#     recordTime.append(TimeNow)
# def run_show8hourPic():
#     plt.close()
#     plt.plot(recordTime,co2Data,linestyle='-', linewidth=1, marker='.', markersize=10, label='CO2')
#     plt.legend()
#     plt.xticks(rotation = 45)
#     plt.show(block=False)
#     plt.pause(3)
# def run_resetData():
#     co2Data=[]
#     recordTime=[]

class driver(Basedriver):
    def Init_pins(self):
        pass

    def __init__(self, pins):
        super(driver, self).__init__(pins)

    def get_data(self):

        co2Data=[]
        recordTime=[]
        with SMBus(0) as bus:
            sgp=Sgp30(bus,baseline_filename="/tmp/mySGP30_baseline")#这句是sgp示例里面写的，我没仔细去看是用来做什么的，可以删掉
            sgp.i2c_geral_call()
            sgp.init_sgp()
            print(sgp.read_measurements()[0][0])
            # schedule.every(10).minutes.do(run_recordData)
            # schedule.every(1).hours.do(run_show8hourPic)
            # schedule.every(24).hours.do(run_resetData)
            # while True:
            #     schedule.run_pending()  # run_pending：运行所有可以运行的任务
            data = {'co2':sgp.read_measurements()[0][0],"time": time.time()}
            return data