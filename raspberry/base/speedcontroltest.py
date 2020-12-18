# -*- coding: UTF-8 -*-
from __future__ import print_function
import RPi.GPIO as GPIO
from multiprocessing import Process,Value
import time
import threading
import encoder
import motor
import uart

#<7.5V : 4.8
# ~8V : 4
retreat_time = 4


def actual_speed():
    print(encoder.cn1)

def pid(data_in,set_value,p,i,d,i_erro = 0):
    max_i_erro = 10
    last_value = 0
    c_erro = data_in - set_value
    i_erro += c_erro*0.01
    i_erro = motor.limiter(i_erro,-max_i_erro,max_i_erro)
    l_erro = last_value - set_value
    data_out = p*c_erro+d*l_erro+i*i_erro
    last_value = data_in
    return data_out
        
        
        
#    para:status_now: moveon为向前，wheel为旋转
def stop_now(status_now):
    done_flag = 0
    if(status_now == 'speed'):
        #直接给向后的速度，让电机急停
        out_speed = 80
        out_direct = 0
        motor.set_car_run(1,out_speed,out_direct)
        time.sleep(1)
##        while True:
##            set_speed = 0
##            speed_p = 40   #encoder and speed
##            speed_d =0 
##            speed_i = 2
##            max_i_erro = 10
##            speed_zero = 0
##            l_speederro = 0   
##            speed_i_erro = 0
##        
##            c_speederro = (2*encoder.array[0]-1) * encoder.array[1] - set_speed
##            speed_i_erro += c_speederro*0.01
##            speed_i_erro = motor.limiter(speed_i_erro,-max_i_erro,max_i_erro)
##            #由pid设置输出速度
##            out_speed = speed_p*c_speederro+speed_d*l_speederro+speed_i*speed_i_erro
##            l_speederro = c_speederro
##            print ('c_speederro:',c_speederro)
##            #当速度为0时，跳出
##            if(c_speederro == 0):
##                done_flag = 1
##                break
##            motor.set_car_run(1,out_speed,out_direct)
        
    elif(status_now == 'direct'):
        #读方向
        l_direct = encoder.array[0]
        out_direct = (2*l_direct-1) * 130       #赋值为相反方向
        out_speed = 0
        motor.set_car_run(1,out_speed,out_direct)
        time.sleep(0.5)
        while True:
            set_direct = 0
            direct_p = 40   #encoder and speed
            direct_d =0 
            direct_i = 2
            max_i_erro = 10
            direct_zero = 0
            l_directerro = 0   
            direct_i_erro = 0
        
            c_directerro = (2*encoder.array[0]-1) * encoder.array[1] - set_direct
            direct_i_erro += c_directerro*0.01
            direct_i_erro = motor.limiter(direct_i_erro,-max_i_erro,max_i_erro)
            out_direct = direct_p*c_directerro + direct_d*l_directerro + direct_i*direct_i_erro
            l_directerro = c_directerro
            print ('c_directerro:' , c_directerro)
            if(c_directerro == 0):
                done_flag = 1
                break
            motor.set_car_run(1,out_speed,out_direct)
        
    return done_flag

def standstill():   #保持静止
    speed_p = 65   #encoder and speed
    speed_d =0 
    speed_i = 2
    max_i_erro = 10
    speed_zero = 0
    set_speed = 0
    last_value = 0
    speed_i_erro = 0
    global SPEED
    global DIRECTION
    global still_flag
    still_flag = 1
    SPEED = 0
    DIRECTION = 0
    while still_flag == 1:
        cs,speedl,speedr = uart.asksignal()
        c_speederro = speedl - set_speed
        speed_i_erro += c_speederro*0.01
        speed_i_erro = motor.limiter(speed_i_erro,-max_i_erro,max_i_erro)
        l_speederro = last_value - set_speed
        out_speed = speed_p*c_speederro+speed_d*l_speederro+speed_i*speed_i_erro
        last_value = speedl
        #time.sleep(0.01)
        if ( speedl or speedr) !=0:
            SPEED = -(out_speed+speed_zero)
            #print("speedcontrol\n",SPEED)
            #print('out_speed%d:' % out_speed)
            motor.set_car_run(1,SPEED,DIRECTION)
        elif ( speedl or speedr) == 0:
            motor.set_car_run(0,0,0)
        #print(encoder.array[1],encoder.array[0])
    if still_flag == 0:
        set_car_run(1,0,0)
        
        
####没改好，别用！！！！！
###改动standstill内容：
##    # 1.主函数传入上一次的设定速度（由于speed_d设为0，传进来也没有用到）
##    # 2.仅返回速度，不设定，取消了死循环
##def standstill_new(l_speed):   #保持静止
##    speed_p = 40   #encoder and speed
##    speed_d =0 
##    speed_i = 2
##    max_i_erro = 10
##    speed_zero = 0
##    set_speed = 0
##    l_speederro = 0     #改动1，原为last_value
##    speed_i_erro = 0
##    global SPEED
##    still_flag = 1
##    SPEED = 0
##    DIRECTION = 0
##    #改动6，去掉循环 while still_flag == 1:
##    c_speederro = (2*array[0]-1) * encoder.array[1] - set_speed
##    #得到偏差i
##    speed_i_erro += c_speederro*0.01
##    speed_i_erro = motor.limiter(speed_i_erro,-max_i_erro,max_i_erro)
##    #得到上一次的偏差
##    l_speederro = l_speed - set_speed       #改动2，原为l_speederro = last_value - set_speed
##    out_speed = speed_p*c_speederro+speed_d*l_speederro+speed_i*speed_i_erro
##    #改动3，注释掉 last_value = encoder.array[1]
##    #time.sleep(0.01)
##    #若当前有速度（与set_speed有偏差）
##    #改动4，原判断语句 if (encoder.array[1] or encoder.array[4]) !=0:
##    # if (c_speederro != 0)
##        # #若此时速度向前
##        # if encoder.array[0] == 1 :
##               # SPEED = -(out_speed+speed_zero)
##        # #若此时速度向后
##        # if encoder.array[0] == 0 :
##               # SPEED = (out_speed+speed_zero)
##           #print("speedcontrol\n",SPEED)
##        #print('out_speed%d:' % out_speed)
##        #改动5，注释掉 motor.set_car_run(1,SPEED,DIRECTION)
##    #若没有速度
##    # elif (encoder.array[1] or encoder.array[4]) == 0:
##    # elif (c_speederro == 0)
##        # SPEED = 0
##        #print(encoder.array[1],encoder.array[0])
##    # if still_flag == 0:
##        # set_car_run(1,0,0)
##    return out_speed
        
def keep_speed(set_speed):   #保持速度，以编码器读数为准
    k1 = 0.2375    #sum and pwm
    speed_p = 0
    speed_d = 0
    speed_i = 0
    max_i_erro = 10
    last_value = 0
    speed_i_erro = 0
    while True:
       real_speed = encoder.array[2]*k1
       c_speederro = real_speed - set_speed
       speed_i_erro = c_speederro*0.01
       speed_i_erro = motor.limiter(speed_i_erro,-max_i_erro,max_i_erro)
       l_speederro = last_value - set_speed
       out_speed = speed_p*c_speederro + speed_d*l_speederro + speed_i*speed_i_erro
       last_value = encoder.array[2]
       if real_speed >= set_speed:
           SPEED = set_speed - out_speed + speed_zero
       elif real_speed < set_speed:
           SPEED = set_speed + out_speed + speed_zero
       motor.set_car_run(1,SPEED,DIRECTION)

def retreat(retreat_speed):  #灭灯后迅速远离灯
    motor.set_car_run(1,retreat_speed,0)
    time.sleep(retreat_time)
    motor.set_car_run(1,-retreat_speed,0)
    time.sleep(1)
    motor.set_car_run(0,0,0)

def speed_con():
    try:      
        encoder.start_encoder()
        
        ##使用线程
        thread_test_motor = threading.Thread(target = motor.test_motor,args = ())
        thread_keep_speed = threading.Thread(target = keep_speed,args = ())
        thread_standstill = threading.Thread(target = standstill,args = ())

        #启动进程
        encoder.process_cout_thread.start()

        #启动线程
        #encoder.thread_cout_thread.start()
        thread_test_motor.start()
        motor.MODE = 4
        #thread_keep_speed.start()
        thread_standstill.start()
        encoder.timer.start()
        
    except KeyboardInterrupt:
        motor.PWM = 0
        motor.DIR = 0

def speedcontrol_test():
    '''
    #thread_encoder = threading.Thread(target = encoder.start_encoder,args = ())
    thread_motor = threading.Thread(target = motor.test_motor,args = ())
    thread_standstill = threading.Thread(target = standstill,args = ())
    #thread_encoder.start()
    thread_motor.start()
    thread_standstill.start()
    '''
    SPEED = 0
    DIRECTION = 0

    motor.init_motor(500)
    motor.stop()
    standstill()
        

def main():
##    encoder.RF_flag = 0
    #encoder.encoder_print_flag = 0
##    encoder.start_encoder()
    #motor.test_motor()
    #speed_con()
    speedcontrol_test()
    #keep_speed()
    
    
if __name__ == "__main__":
    try:
        main()
    finally:
        process_count_thread.stop()
        process_timer.stop()
        thread_motor.stop()
        thread_standstill.stop()
        GPIO.cleanup();
        
    

    
