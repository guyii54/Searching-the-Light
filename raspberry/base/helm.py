#-*-coding:utf-8-*-
import RPi.GPIO as GPIO
import time
import numpy as np
import numpy

SIG = 7    #信号线引脚
CYCLE = 50  #频率50Hz，周期20ms
helmin = 5.2
helmout = 11
SIN_L = 14  #左红外
SIN_R = 15  #右红外

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

def RF_read():
     out_l = GPIO.input(SIN_L)
     out_r = GPIO.input(SIN_R)
     RF_result = out_l and out_r
     return RF_result     

def helm_out(helm_h):
    helm_h.ChangeDutyCycle(helmout)

def helm_in(helm_h):
    helm_h.ChangeDutyCycle(helmin)

def main():
    angle = 10
    helm_h = initial_helm()
##    initial_RF()
    while True:
        helm_out(helm_h)
        print 'out'
        time.sleep(2)
        helm_in(helm_h)
        print 'in'
        time.sleep(2)
##    while True:
####        print RF_read()
##        angle = input('enter angle:')
##        helm_h.ChangeDutyCycle(angle)
##        print(angle)


if __name__ == "__main__":
    try:
        main()
    finally:
        GPIO.cleanup()

