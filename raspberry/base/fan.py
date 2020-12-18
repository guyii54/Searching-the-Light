#-*-coding:utf-8-*-
import RPi.GPIO as GPIO
import time
import numpy as np
import numpy

FAN_PIN = 0
CYCLE = 50


def initial_fan():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(FAN_PIN,GPIO.OUT)
    GPIO.output(FAN_PIN,1)
##    fan_h = GPIO.PWM(FAN_PIN,CYCLE)    #设置周期
##    fan_h.start(50)
##    fan_h.ChangeDutyCycle(50)


initial_fan()
