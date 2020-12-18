# -*- coding: utf-8 -*-
import time
import picamera
import cv2
import io
import numpy as np
import img
import matplotlib.pyplot as plt
import motor
import encoder
import speedcontrol
import traceback
import helm

#6.16
#add fan
#add high direct before moving in status1
#add high speed before moving in status2
#add black tap on RF



status = 0
speed= 0
direct = 0
mode = -1
l_center = 0
status2_speed = 70
IR_flag = 1
status3_flag = 0
status1_flag = 0
status2_flag = 0

    #direct >0,turn left
bias_thresh = 100
    #when in status1 c_center[0] and WIDTH/2's distance <= bias_thresh,change into status2
dis_thresh = 50
    #when in status2 c_center[1] <= HEIGHT-dis_thresh,chan into status3

#*******status1 values
comfirm_get = 20
wh_direct = 130

#*********initial camera***********
HEIGHT = 240
WIDTH = 320
FPS = 90
BRIGHTNESS = 50
camera = picamera.PiCamera()
camera.resolution = (WIDTH,HEIGHT)
camera.framerate = FPS
camera.brightness = BRIGHTNESS
camera.shutter_speed = 800      #快门速度
camera.exposure_compensation = 25
camera.ISO = 1300
camera.exposure_mode = 'sports'

##camera.awb_mode = 'fluorescent'

stream = io.BytesIO()
##camera.close()



#初始化电机
motor.init_motor(500)
motor.stop()
motor.car_run_flag = 1

#初始化编码器
#encoder.start_encoder()


#初始化红外
motor.init_IR()

#初始化舵机
helm.initial_RF()
helm_h = helm.initial_helm()
helm.helm_in(helm_h)

print 'initial done'


##while True:          ##红外
##    if (motor.get_IRKey() == 0x45):
##        motor.set_car_run(1,5,0)
##        print("stop!")
while True:
    #time.sleep(0.1)
    if (motor.get_IRKey() == 0x46):
        status = 1
        print("start!")
        break


#test
last_direct = 0
try:
##    fp = 0
##    motor.set_car_run(1,0,130)
##    time.sleep(3)
##    s = time.time()
    
    for foo in camera.capture_continuous(stream,'jpeg',use_video_port=True):
##        s = time.time()


                
        data = np.fromstring(stream.getvalue(),dtype=np.uint8)
        c_img = cv2.imdecode(data,cv2.CV_LOAD_IMAGE_UNCHANGED)
##        cv2.imwrite('/home/pi/final/final_test/capture'+str(fp)+'.jpg',c_img)

        
##        fp+=1
##        cv2.imshow('c_img',c_img)
##        cv2.waitKey(10)
        
      
        
        
            
            
        #状态是否发生改变
        if(status==1):
            c_red = img.red_bgr(c_img)
            c_red = img.change_binary(c_red)
            c_center,red_num = img.get_center(c_red)
##            cv2.imshow('c_red',c_red)
##            cv2.waitKey(10)
            #print('num')
##            print(num,encoder.array[:])
##            print 'red_number:',red_num
##            print 'center:',c_center
            
            if ((red_num > comfirm_get) and (abs(c_center[0] - WIDTH/2) < bias_thresh)):
                status = 2
                status2_flag = 0
                #停止电机
##                speedcontrol.stop_now('direct')
                motor.set_car_run(1,0,(-wh_direct)*1.5)
                time.sleep(0.2)
##                print('staues1 done')  
                motor.set_car_run(0,0,0)
            #当红点数大于阈值且灯重心距离足够近
            
            
        if(status == 2):
##             if(speedcontrol.stop_now('direct') == 1):
##                    print('stop done')
##            print('status2,c_center:')
##            print(c_center)
##            print('done')
##            e = time.time()
##            print(fp/(e-s))
            c_red = img.red_bgr(c_img)
            c_red = img.change_binary(c_red)
            c_center,red_num = img.get_center(c_red)
            #print("statues2:")
            if(c_center[1] >= HEIGHT-dis_thresh):
                #speed_tmp = 1.0/(c_center[0][1]*0.0001)
##                print("hight is ok")
##                arr = encoder.array[:]
##                print arr
##                speed_tmp = -encoder.array[1]
##                speed_tmp = motor.limiter(speed_tmp,-150,150)
##                helm.helm_out(helm_h)
                motor.set_car_run(1,30,0)
##                time.sleep(0.1)
##                print ("speed_tmp is",speed_tmp)
                while True:
                    if (helm.RF_read() == 0):
                        #speedcontrol.stop_now(speed)
    ##                    motor.set_car_run(1,-100,0)
    ##                    time.sleep(0.5)
    ##                    speed_tmp = -encoder.array[1]
    ##                    speed_tmp = motor.limiter(speed_tmp,-150,150)
    ##                    motor.set_car_run(1,speed_tmp,0)
    ##                    print ("speed_tmp is",speed_tmp)
##                        print 'RF is on!'
                        helm.helm_out(helm_h)
                        motor.set_car_run(1,-488,0)
                        time.sleep(0.1)
                        status = 3
                        motor.set_car_run(0,0,0)
                        time.sleep(2)
##                        print("staues2 is done!")
                        break
##                    print 'status2 is not done!'
            elif(c_center[1] < 0 ):
                    motor.set_car_run(1,-80,0)
                    time.sleep(1)
                    motor.set_car_run(0,0,0)
                    status = 1
                    status1_flag = 0
                    wh_direct = -wh_direct
        #status3：灭灯，后退
        if(status == 3):
            if(status3_flag == 1):
                status = 1
                status1_flag = 0
                status3_flag = 0
##                print 'status3 is done!'











        #状态内执行
        if(status == 1):
            if(status1_flag >= 4):
                direct = wh_direct
            else:
                direct = wh_direct+15
            speed = 0
            status1_flag += 1
            motor.set_car_run(1,speed,direct)
##            print 'speed:',encoder.array[:]
##            speedcontrol.standstill()
   
        
        if(status == 2):
            if(status2_flag >= 4):
                speed = status2_speed
            else:
                speed = status2_speed+10
            out_direct = speedcontrol.pid(c_center[0]+1,WIDTH/2,1,0,0)
##                if (last_direct > 0) and (out_direct < 0):
##                    out_direct = -out_direct
##                if (out_direct != last_direct) and (out_direct < -100):
##                    last_direct = out_direct
##                print("last_direct",last_direct)
            out_direct = motor.limiter(out_direct,-30,30)
            motor.set_car_run(1,speed,out_direct)
            status2_flag += 1
##            print 'status2',c_center,out_direct,red_num
                
                
        if(status == 3):
##            helm.helm_out(helm_h)
##            time.sleep(2)
            helm.helm_in(helm_h)
            time.sleep(0.1)
            speedcontrol.retreat(-80)
            status3_flag = 1
##            
##    print('current status:%d' % status)
##    
##    if(status == 3):
##        motor.stop()
##        real_speed = encoder.array[1]
##        print('real_speed:',real_speed)
##        
##    else:
##        print('done')
####        break
##        
    
        stream.truncate()
        stream.seek(0)
##        e= time.time()
##        print(e-s)

##    e= time.time()
    camera.close()
##    print (fp/(e-s))

finally:
    camera.close()
    motor.set_car_run(0,0,0)
##    e = time.time()
##    print 'fps:', fp/(e-s)
    print traceback.print_exc()
    
    
    
    
    
    
