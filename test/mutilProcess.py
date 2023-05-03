#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/3 19:02
# @Author  : 李帅兵
# @FileName: mutilProcess.py
# @Software: PyCharm
from multiprocessing import Process
import os
import time


class Process_Test(Process):
    def __init__(self, interval):
        Process.__init__(self)
        self.interval = interval

    # 重写run方法
    def run(self):
        print('子进程%d,父进程%d' % (os.getpid(), os.getppid()))
        t_start = time.time()
        time.sleep(self.interval)
        t_stop = time.time()
        print('%s执行结束，耗时%0.2f' % (os.getpid(), t_stop - t_start))


if __name__ == '__main__':
    p = Process_Test(2)
    p.start()
    print(p.is_alive())
    p.join()
    print('主进程%s' % os.getpid())
    print(p.is_alive())
