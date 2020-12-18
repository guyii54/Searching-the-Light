#-*-coding:utf-8-*-
import RPi.GPIO as GPIO
import time
import numpy as np
import numpy

SIG = 7    #信号线引脚
CYCLE = 50  #频率50Hz，周期20ms
SIN_L = 14
SIN_R = 15

def initial_helm():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(SIG,GPIO.OUT)
    helm_h = GPIO.PWM(SIG,CYCLE)    #设置周期
    helm_h.start(0)     #占空比设为0
    return helm_h

def initial_RF():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(SIN_L,GPIO.IN,GPIO.PUD_DOWN)
    GPIO.setup(SIN_R,GPIO.IN,GPIO.PUD_DOWN)


angle = 10
helm_h = initial_helm()
initial_RF()
while True:
##    angle = input('enter angle:')
##    helm_h.ChangeDutyCycle(angle)
##    print(angle)
    out_l = GPIO.input(SIN_L)
    out_r = GPIO.input(SIN_R)
    print(out_l,out_r)
