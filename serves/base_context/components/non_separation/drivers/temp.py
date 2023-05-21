#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/23 10:34
# @Author  : 李帅兵
# @Project : brilliant_clustering
# @File    : temp.py
# @Software: PyCharm
import time

import RPi.GPIO as GPIO

PWM = 21
SWITCH = 26
global p
global now_light
def Init():
    global p, now_light
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(PWM, GPIO.OUT)
    GPIO.setup(SWITCH,GPIO.OUT)
    GPIO.output(SWITCH,GPIO.LOW)
    GPIO.output(PWM, GPIO.LOW)
    # GPIO.output(pin, GPIO.LOW)
    p = GPIO.PWM(PWM, 500)
    p.start(0)
    now_light = 0


def power_on():
    global p
    p.ChangeDutyCycle(100)


def set_light(brightness):
    global p
    p.ChangeDutyCycle(brightness)
    '''
    global p, now_light
    
    GPIO.setup(SWITCH,GPIO.OUT)
    if lightness > now_light:
        try:
            for i in range(now_light + 1, lightness + 1):
                time.sleep(0.00002)
                p.ChangeDutyCycle(i)
        except Exception as e:
            for i in range(now_light - lightness):
                time.sleep(0.00002)
                p.ChangeDutyCycle(now_light - i)
    else:
        try:
            for i in range(now_light+1 - lightness):
                time.sleep(0.00002)
                p.ChangeDutyCycle(now_light - i)
        except Exception as e:
            for i in range(now_light + 1, lightness + 1):
                time.sleep(0.00002)
                p.ChangeDutyCycle(i)
    
    
    now_light = lightness
'''
def power_off():
    global p
    p.ChangeDutyCycle(0)


def Test_run():
    power_on()
    time.sleep(4)
    power_off()
