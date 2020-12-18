# -*- coding: utf-8 -*-
import time
import picamera
import cv2
import io
import numpy as np
import img
##import matplotlib.pyplot as plt
import motor
##import encoder
import speedcontrol
import traceback
##import helm
##import beep
import uart
import serial

#6.16
#add fan
#add high direct before moving in status1
#add high speed before moving in status2
#add black tap on RF

#7.18
#按照流程图重写了总程序，整理了各个常量和全局变量
#编码器做闭环的pid算法封装在set_car_run()中
#图像做闭环的pid方向控制写在主程序中
#五个星号#的注释为调试用的代码，最后运行时可删去
#暂定避障传感器用红外，制动传感器用超声

##real max cs_thresh : 1462


#全局常量-阈值
red_num_thresh = 15      #红点数量足够多
dis_xy_thresh = 20       #确认为圆形
bias_thresh = 140        #确认重心在中心线
dis_thresh = 150         #确认距离足够近
cs_thresh = 1200         #超声波阈值，制动距离
stop_thresh = 5          #认为已经停下
dis_x_thresh = 70                           #改过

#全局常量-速度、方向，全部待调试
st1_direct = 250         #status1后退旋转方向值
st1_accelerate = 0
st1_speed =  0       #status1后退旋转速度值
st2_speed = 150           #status2前进速度值               ##改过
st2_direct_limmiter = 130
st2_accelerate = 20      #status2加速值   20               ##改过
st3_speed = 20         #status3极小的滑行速度
st5_flag = -1            #status5入口选择
st5_0_direct = 100       #status5原地旋转方向值
st5_0_speed = 100        #status5原地旋转后速度值
st5_0_whtime = 1         #status5旋转时间
st5_1_direct = 50        #status5有速度的转弯方向值
st5_1_whtime = 2         #status5转弯时间
st5_timeout = 2          #status5超时时间

k_direct_stop = 2.5

k_speed_stop1 = -6
k_speed_stop2 = -1

k_img_direct = 0.7

st3_k_img_direct = 0.9
st3_direct_limmiter = 150




#全局变量-标识符、缓存器
status = 1            #状态标识符
speed= 0                #当前速度
fb_speed = 0            #feedback speed反馈回的速度
direct = 0              #当前方向
accelerate = 0          #加速启动标识符
rf = [0,0,0,0]       #红外信号,依次为左前，右前，左中，右中
picture = 0




#*********initial camera***********
HEIGHT = 240
WIDTH = 320
FPS = 90
BRIGHTNESS = 50
##camera = picamera.PiCamera()
##camera.resolution = (WIDTH,HEIGHT)
##camera.framerate = FPS
##camera.brightness = BRIGHTNESS
##camera.shutter_speed = 800      #快门速度
##camera.exposure_compensation = 25
##camera.ISO = 1300
##camera.exposure_mode = 'sports'

##camera.awb_mode = 'fluorescent'

cap = cv2.VideoCapture(0)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)

##stream = io.BytesIO()
##camera.close()



#初始化电机
motor.init_motor(500)
motor.stop()
motor.car_run_flag = 1



#初始化红外
##motor.init_IR()



##beep.initial_beep()
##num = 0
##while True:
##    ret,c_img = cap.read()
##    num += 1
##    if(num>100):
##        break


##beep.beep_once()
print 'initial done'


def standstill_img(speed,cs_thresh):   #保持静止
    uart.startcs()
##    time.sleep(0.01)
    speed_p = -80   #encoder and speed 250
    speed_d = 0 
    speed_i = 0     #4
    max_i_erro = 10
    speed_zero = 0
    set_speed = speed
    last_value = 0
    speed_i_erro = 0
    speed = 0
    direct = 0
    times = 0
    while True:
##        times+=1
        cs,speedl,speedr = uart.askcs()
##        print speedl
        if speedr == -1:
            speedl = 0
            speedr = 0
##        print (speedl,speedr)
        c_speederro = speedr - set_speed
        speed_i_erro += c_speederro*0.01
        speed_i_erro = motor.limiter(speed_i_erro,-max_i_erro,max_i_erro)
        l_speederro = last_value - set_speed
        out_speed = speed_p*c_speederro+speed_d*l_speederro+speed_i*speed_i_erro
        last_value = speedr
        speed = (out_speed+speed_zero)
        
        ret,c_img = cap.read()
        c_red = img.red_bgr(c_img)
        c_red = img.change_binary(c_red)
        c_center,red_num,dis_xy,dis_x= img.get_center_new(c_red)
        direct = st3_k_img_direct * (c_center[0]-((WIDTH/2)))
        direct = motor.limiter(direct,-st3_direct_limmiter,st3_direct_limmiter)
##                    print 'direct:',direct
        #time.sleep(0.01)
##        if (abs(speedl - set_speed) >= 10):
        speed = (out_speed+speed_zero)
##            print("speedcontrol\n",SPEED)
##            print('out_speed:',out_speed)
        motor.set_car_run(1,speed,direct)
##        else:
##            motor.set_car_run(1,set_speed,0)
##        else:
##            times += 1
##            if (times > 20):
        if (cs!=0) and (cs <cs_thresh):                ##改过
            print 'cs1:',cs,c_center[1]
            motor.set_car_run(1,0,0)
##            print times
##                motor.set_car_run(1,45,0)
            break
        #print(encoder.array[1],encoder.array[0])


try:
    fp = 0
    s = time.time()
    
    while True:
        fp += 1

        
        if status == 1:
            ret,c_img = cap.read()
            picture += 1
            c_red = img.red_bgr(c_img)
            c_red = img.change_binary(c_red)
            #得到最大红色连通域重心坐标，面积，横半径与纵半径
            c_center,red_num,dis_xy,dis_x = img.get_center_new(c_red)
            #转status1?
            #yes
            if ((red_num > red_num_thresh) and (dis_xy < dis_xy_thresh) and (abs(c_center[0] - WIDTH/2) < bias_thresh)):
                #注：这里没有加流程图中停电机的动作，直接给了大speed
                   #####
##                motor.set_car_run(1,0,0)
##                time.sleep(0.01)
##                while True:
##                    print '1'
##                print 'find'
                picture = 0
                print c_center,red_num,dis_xy,dis_x
                status = 2  #2
                speedcontrol.wheelstop()
##                time.sleep(4)
##                print 'done'
                continue
            if picture >= 300:
                break

            #no
            direct = st1_direct
            speed = st1_speed
            motor.set_car_run(1,speed,direct)
            
            
        elif status == 2:
            ret,c_img = cap.read()
            c_red = img.red_bgr(c_img)
            c_red = img.change_binary(c_red)
            c_center,red_num,dis_xy,dis_x= img.get_center_new(c_red)
            if (red_num < red_num_thresh):
                st1_direct = -st1_direct
                status = 1
                continue
##            print 'c_center:',c_center
##            if c_center == [-1,-1]:
##                break
            #转status3?
            #yes
            if ((dis_x > 60)and (dis_x<1000)):
                print 'status2 to status3'    #####
                status = 3 
                continue
            #no
            else:
                rf ,speedl,speedr = uart.asksignal()
##                print rf,speedl,speedr
                #转status5?
                #yes
##                if rfsgl == 1111:      ####
##                    st5_flag = 1
##                    status = 5
##                    continue
                #no
##                else:
                    #加速是否完成
##                    rfi,fb_speed,speedr = uart.asksignal()
                if fb_speed >= st2_speed:
                    speed = st2_speed
                else:
                    speed = st2_speed + st2_accelerate
                #图像做闭环的pid方向控制（需要改）
                direct = k_img_direct * (c_center[0]-((WIDTH/2)))
                direct = motor.limiter(direct,-st2_direct_limmiter,st2_direct_limmiter)
##                    print 'direct:',direct
                motor.set_car_run(1,speed,direct)
                    
                    
        elif status == 3:
            speed = st3_speed
##            motor.set_car_run(1,speed,0)
            standstill_img(speed,cs_thresh)
##            rf,speedl,speedr = uart.asksignal()
##            motor.set_car_run(1,speed,0)
##            print 'slow'
            #小速度滑行，等待制动距离
            speedcontrol.cs_stop()
##            print 'start cs'
##            while True:
##                cs,speedl,speedr = uart.askcs()
####                print 'cs:',cs
##                if (cs != 0):
##                    if (cs<cs_thresh):
##                        uart.endcs()
##                        print 'cs done'
##                        speedcontrol.stop(0)
##                        time.sleep(0.3)
##                        break
            #急停，等待速度为0
            status = 4
            print 'status3 to 4'
                    
                    
        elif status == 4:
##            times4 = 0
            uart.usehelm()
            time.sleep(1.5)
##            print 'start 4'
##            while (times4 < 3):
##                uart.usehelm()
##                print 'use helm'
##                times4 += 1
##                time.sleep(1.5)
##                ret,c_img = cap.read()
##                c_red = img.red_bgr(c_img)
##                c_red = img.change_binary(c_red)
##                c_center,red_num,dis_xy,dis_x = img.get_center_new(c_red)
##                if (red_num < red_num_thresh):
##                    break
            speed = -150
            #break   ####
            motor.set_car_run(1,speed,0)
            time.sleep(2.3)
            motor.set_car_run(1,0,0)
            status = 1
            c_center = [-1,-1]
            red_num = 0
            dis_xy = 0
            dis_x = 0
            while (picture < 10):
                picture += 1
                ret,c_img = cap.read()
                c_red = img.red_bgr(c_img)
                c_red = img.change_binary(c_red)
            picture = 0
            print 'status4 to status1'
    
            

            #转status1?
            #yes
##            if (red_num < red_num_thresh):
##                status = 1
##                continue
##            else:
                #此处判断条件待定
                #转status5？
                #yes
##                if (red_num < close_red_num):
##                    status = 5
##                    st5_flag = 0
##                    continue
                #no 
                #抖动向前不太好，易撞灯
            
                
                
##        elif status == 5:
##            #从status4进入
##            if st5_flag == 0:
##                direct = st5_0_direct
##                set_car_run(1,0,direct)
##                time.sleep(st5_0_whtime)
##                #已旋转一定角度，设置speed前进
##                speed = st5_0_speed
##                direct = -direct
##                set_car_run(1,speed,direct)
##                st5ts = time.time()     #st5 time start
##                while True:
##                    ret,c_img = cap.read()
##                    c_red = img.red_bgr(c_img)
##                    c_red = img.change_binary(c_red)
##                    c_center,red_num,dis_xy,dis_x = img.get_center_new(c_red)
##                    #7.转statu2?
##                    #yes
##                    if (red_num > red_num_thresh):
##                        status = 2
##                        break
##                    #no
##                    else:
##                        #8.转status1，已超时
##                        #yes
##                        st5te = time.time()
##                        if ((st5te - st5ts) > st5_timeout):
##                            status = 1
##                            break
                    
                    
            
            
            
            
            
        

finally:
##    camera.close()
    motor.set_car_run(1,0,0)
    e = time.time()
##    beep.beep_once()
    print 'fps:', fp/(e-s)
    print traceback.print_exc()
    
    
    
    
    
    
