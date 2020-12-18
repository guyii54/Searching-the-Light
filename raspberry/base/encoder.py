# -*- coding: utf-8 -*-
from __future__ import print_function
import RPi.GPIO as GPIO
import time
import threading
from multiprocessing import Process,Array
import os

#left encoder
LSB1 = 17
Dir1 = 27
Z1 = 22
#right encoder
LSB2 = 25
Dir2 = 23
Z2 = 24

#global value
#global Dir_left

def initial_encoder():
    global A1,B1,Z1,A2,B2,Z2
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(LSB1,GPIO.IN,GPIO.PUD_UP)
    GPIO.setup(Dir1,GPIO.IN,GPIO.PUD_UP)
    GPIO.setup(Z1,GPIO.IN,GPIO.PUD_UP)
    GPIO.setup(LSB2,GPIO.IN,GPIO.PUD_UP)
    GPIO.setup(Dir2,GPIO.IN,GPIO.PUD_UP)
    GPIO.setup(Z2,GPIO.IN,GPIO.PUD_UP)

def encoderZ1(Z1):
    global array
    if array[0] == 1:
         array[2] += 1
    elif array[0] ==0:
        array[2] -=1

def encoderLSB1(LSB1):
    global array
    array[1] += 1

def encoderZ2(Z2):
    global array
    if array[3] ==1:
        array[5] += 1
    elif array[3] ==0:
        array[5] -= 1
    

def encoderLSB2(LSB2):
    global array
    array[4] += 1


def cout_thread(array):  #计数线程
    GPIO.add_event_detect(LSB1,GPIO.RISING,encoderLSB1)
    GPIO.add_event_detect(Z1,GPIO.RISING,encoderZ1)
    GPIO.add_event_detect(LSB2,GPIO.RISING,encoderLSB2)
    GPIO.add_event_detect(Z2,GPIO.RISING,encoderZ2)
    while True:         #防止进程被杀死
        pass            #空语句
    
def test_process():
    while True:
        print("alive")

def _timer_process(array):
    global inter_time
    inter_time = 0.1   #定时器定时间隔s
    while True:
        time.sleep(inter_time)
        fun_timer()

def fun_timer():    #定时器线程/进程共享数组
                                            #array[0]=Dir_left,array[1]=cn1,
                                            #array[2]=pulse_sum_left,array[3]=Dir_right,
                                            #array[4]=cn2,array[5]=pulse_sum_right
    global array
    global encoder_print_flag

    if encoder_print_flag == 1:
        print(array[:])

    array[0] = -1   #Dir_left
    array[1] = 0    #cn1
    array[2] = 0    #sum_left
    array[3] = -1   #Dir_right
    array[4] = 0    #cn2
    array[5] = 0    #sum_right
    
    array[0] = GPIO.input(Dir1)     #Dir_left
    temp = GPIO.input(Dir2)
    array[3] = 1 - temp             #Dir_right

def start_encoder():    #外部文件调用函数
    global array
    array = Array("l",[0,0,0,0,0,0])
    global encoder_print_flag
    encoder_print_flag = 0
    global timer
    global process_count_thread
    initial_encoder()
    
    process_count_thread = Process(target = cout_thread, args = (array,))
    process_timer = Process(target = _timer_process, args = (array,))
    process_count_thread.start()
    process_timer.start()
    
def test_encoder(): #测试函数
    global timer
    global process_count_thread
    global process_timer
    initial_encoder()
    try:
        process_count_thread = Process(target = cout_thread, args = (array,))
        process_timer = Process(target = _timer_process, args = (array,))
        process_count_thread.start()
        process_timer.start()
    except KeyboardInterrupt:
        GPIO.cleanup();
        

def main():     #主函数
    global array
    array = Array("l",[0,0,0,0,0,0])
    #print(array[:])
    #test_process = Process(target = test_process,args = ())
    #test_process.start()
    
    global encoder_print_flag
    encoder_print_flag = 1
    test_encoder()
    '''
    while True:
        print ("process_count_thread.pid:",process_count_thread.pid)
        print ("process_count_thread.name:",process_count_thread.name)
        print ("process_count_thread.is_alive:",process_count_thread.is_alive())
        print ("process_timer.is_alive:",process_timer.is_alive())
        time.sleep(0.2)
    '''

if __name__ == "__main__":
     main()
    #start_encoder()
    

    
