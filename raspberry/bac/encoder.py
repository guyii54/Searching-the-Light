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
    #GPIO.setup(LSB1,GPIO.OUT   #test
    GPIO.setup(Dir1,GPIO.IN,GPIO.PUD_UP)
    GPIO.setup(Z1,GPIO.IN,GPIO.PUD_UP)
    GPIO.setup(LSB2,GPIO.IN,GPIO.PUD_UP)
    GPIO.setup(Dir2,GPIO.IN,GPIO.PUD_UP)
    GPIO.setup(Z2,GPIO.IN,GPIO.PUD_UP)

def encoderZ1(Z1):
    #global pulse_sum_left
    #pulse_sum_left += 1
    global array
    if array[0] == 1:
         array[2] += 1
    elif array[0] ==0:
        array[2] -=1

def encoderLSB1(LSB1):
    #global cn1
    #cn1 += 1
    global array
    array[1] += 1

def encoderZ2(Z2):
    #global pulse_sum_right
    #pulse_sum_right += 1
    global array
    if array[3] ==1:
        array[5] += 1
    elif array[3] ==0:
        array[5] -= 1
    

def encoderLSB2(LSB2):
    #global cn2
    #cn2 += 1
    global array
    array[4] += 1
    '''
    for i in range(5):
        GPIO.output(LSB1,1)
        time.sleep(0.05)
        GPIO.output(LSB1,0)
        '''


def cout_thread(array):  #计数线程
    #test
    #print("cout_thread is running\n")
    #array[2] = 100
    GPIO.add_event_detect(LSB1,GPIO.RISING,encoderLSB1)
    GPIO.add_event_detect(Z1,GPIO.RISING,encoderZ1)
    GPIO.add_event_detect(LSB2,GPIO.RISING,encoderLSB2)
    GPIO.add_event_detect(Z2,GPIO.RISING,encoderZ2)
    while True:         #防止进程被杀死
        pass    #空语句
    
def test_process():
    while True:
        print("alive")

def _timer_process(array):
    #print("OK1")
    global inter_time
    inter_time = 0.1   #定时器定时间隔s
    while True:
        time.sleep(inter_time)
        fun_timer()

def fun_timer():    #定时器线程/进程共享数组
                                            #array[0]=Dir_left,array[1]=cn1,
                                            #array[2]=pulse_sum_left,array[3]=Dir_right,
                                            #array[4]=cn2,array[5]=pulse_sum_right
    #使用数组后无须定义以下变量
    '''
    global cn1
    global cn2
    global pulse_sum_left
    global pulse_sum_right
    global Dir_left
    global Dir_right
    '''
    #print("OK")
    global array
    #global inter_time
    global encoder_print_flag
    #inter_time = 0.1   #定时器定时间隔s

    if encoder_print_flag == 1:
        #print(Dir_left, cn1,pulse_sum_left, Dir_right, cn2, pulse_sum_right)
        #print("{}{}{}{}{}{}\n".format(array[0], array[1], array[2], array[3], array[4], array[5]),end='')
        #print(array[0], array[1], array[2], array[3], array[4], array[5])
        print(array[:])

    array[0] = -1#Dir_left
    array[1] = 0#cn1
    array[2] = 0#sum_left
    array[3] = -1#Dir_right
    array[4] = 0#cn2
    array[5] = 0#sum_right
    
    array[0] = GPIO.input(Dir1)     #Dir_left
    temp = GPIO.input(Dir2)
    array[3] = 1 - temp        #Dir_right
    '''
    Dir_left = -1
    cn1 = 0
    Dir_right = -1
    cn2 = 0

    Dir_left = GPIO.input(Dir1)
    temp = GPIO.input(Dir2)
    Dir_right = 1 - temp 
    '''

    
    #test
    '''
    for i in range (10): 
        GPIO.output(LSB1,1)
        time.sleep(0.01)
        GPIO.output(LSB1,0) 
    '''
    '''
    global timer
    timer = threading.Timer(inter_time, fun_timer)  #循环调用自己
    timer.start()
    '''

def start_encoder():    #外部文件调用函数
    global array
    array = Array("l",[0,0,0,0,0,0])
    #print(array[:])
    global encoder_print_flag
    encoder_print_flag = 0
    global timer
    global process_count_thread
    initial_encoder()
    #try to new a process in the speedcontrol.py
    
    process_count_thread = Process(target = cout_thread, args = (array,))
    process_timer = Process(target = _timer_process, args = (array,))
    process_count_thread.start()
    process_timer.start()

    #below uses thread
    '''
    global Dir_left
    global Dir_right
    global cn1
    global cn2
    global pulse_sum_left
    global pulse_sum_right
    global process_cout_thread
    global thread_cout_thread
    global test_process
    global timer
    initial_encoder()

    Dir_left = 0
    Dir_rihgt = 0
    time.sleep(0.1)

    cn1 = 0  #Initial counter number
    cn2 = 0 
    pulse_sum_left = 0
    pulse_sum_right = 0
    Dir_left = -1
    Dir_right = -1

    try:
        thread_cout_thread = threading.Thread(target = cout_thread,args = ())
        process_cout_thread = Process(target = cout_thread,args = ())
        test_process = Process(target = test_process,args = ())
        timer = threading.Timer(1,fun_timer)
        #process_cout_thread.start()
        #timer.start()
        
    except KeyboardInterrupt:
        GPIO.cleanup();
    '''
    
def test_encoder(): #测试函数
    global timer
    '''
    global Dir_left
    global Dir_right
    global cn1
    global cn2
    global pulse_sum_left
    global pulse_sum_right
    global thread_cout_thread
    '''
    global process_count_thread
    global process_timer
    initial_encoder()
    '''
    Dir_left = 0
    Dir_rihgt = 0
    time.sleep(0.1)
    
    cn1 = 0  #Initial counter number
    cn2 = 0 
    pulse_sum_left = 0
    pulse_sum_right = 0
    Dir_left = -1
    Dir_right = -1
    '''
    try:
        #thread_cout_thread = threading.Thread(target = cout_thread,args = ())
        process_count_thread = Process(target = cout_thread, args = (array,))
        #fun_timer()
        process_timer = Process(target = _timer_process, args = (array,))
        #thread_cout_thread.start()
        process_count_thread.start()
        process_timer.start()
    except KeyboardInterrupt:
        GPIO.cleanup();
        

def main():     #主函数
    #global process_count_thread
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
    

    
