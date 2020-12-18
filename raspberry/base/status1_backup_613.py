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

status = 1
speed= 0
direct = 0
mode = -1
l_center = 0
statues2_speed = 80
IR_flag = 1

    #direct >0,turn left
bias_thresh = 100
    #when in status1 c_center[0] and WIDTH/2's distance <= bias_thresh,change into status2
dis_thresh = 70
    #when in status2 c_center[1] <= HEIGHT-dis_thresh,chan into status3

#*******status1 values
comfirm_get = 10
wh_direct = 120

#*********initial camera***********
HEIGHT = 240
WIDTH = 320
FPS = 90
BRIGHTNESS = 50
camera = picamera.PiCamera()
camera.resolution = (WIDTH,HEIGHT)
camera.framerate = FPS
camera.brightness = BRIGHTNESS
camera.shutter_speed = 800
camera.exposure_compensation = 25
camera.ISO = 1300
camera.exposure_mode = 'sports'

##camera.awb_mode = 'fluorescent'

stream = io.BytesIO()
##camera.close()



#*********initial motor and encoder*************
motor.init_motor(500)
motor.stop()
encoder.start_encoder()
motor.init_IR()
helm.initial_RF()
helm.initial_helm()
motor.car_run_flag = 1

#test
last_direct = 0
try:
    fp = 0
    #motor.set_car_run(1,0,150)
    #time.sleep(3)
    s = time.time()
    for foo in camera.capture_continuous(stream,'jpeg',use_video_port=True):
##        s = time.time()
        data = np.fromstring(stream.getvalue(),dtype=np.uint8)
        c_img = cv2.imdecode(data,cv2.CV_LOAD_IMAGE_UNCHANGED)
##        cv2.imwrite('/home/pi/final/final_test/capture'+str(fp)+'.jpg',c_img)

        
        fp+=1
##        cv2.imshow('c_img',c_img)
##        cv2.waitKey(10)
        
        if (motor.get_IRKey() == 0x45):
            motor.set_car_run(0,0,0)
            while True:
                #time.sleep(0.1)
                if (motor.get_IRKey() == 0x46):
                    status = 1
                    print("restart!")
                    break
            print("stop!")

        if(status==1):
            c_red = img.red_bgr(c_img)
            c_red = img.change_binary(c_red)
            c_center,red_num = img.get_center(c_red)
##            cv2.imshow('c_red',c_red)
##            cv2.waitKey(10)
            #print('num')
##            print(num,encoder.array[:])
            print 'red_number:',red_num
            print 'center:',c_center
            
            if ((red_num > comfirm_get) and (abs(c_center[0] - WIDTH/2) < bias_thresh)):
                status = 2
                #停止电机
                #speedcontrol.stop_now('direct')
                print('staues1 done')  
                motor.set_car_run(0,0,0)
            #当红点数大于阈值且灯重心距离足够近











        
        if(status == 1):
            direct = wh_direct
            speed = 0
            motor.set_car_run(1,speed,direct)
##            print 'speed:',encoder.array[:]
##            speedcontrol.standstill()
   
        
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
                print("hight is ok")
                speed_tmp = 40
                motor.set_car_run(1,speed_tmp,0)
                if (helm.RF_read() == 0):
                    #speedcontrol.stop_now(speed)
                    motor.set_car_run(1,-80,0)
                    time.sleep(1)
                    status = 3
                    motor.set_car_run(0,0,0)
                    print("staues2 is done!")
                    break
            else:
                out_direct = speedcontrol.pid(c_center[0]+1,WIDTH/2,2.2,0,0)

##                if (last_direct > 0) and (out_direct < 0):
##                    out_direct = -out_direct
##                if (out_direct != last_direct) and (out_direct < -100):
##                    last_direct = out_direct
##                print("last_direct",last_direct)
                out_direct = motor.limiter(out_direct,-50,50)
                motor.set_car_run(1,statues2_speed,out_direct)
                print(c_center,out_direct,red_num)
                status = 2
                
##    if(status == 3):
##        if(real_speed == 0):
##            status = 4
##        else:
##            status = 3
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

    e= time.time()
    camera.close()
    print (fp/(e-s))

finally:
    camera.close()
    motor.set_car_run(0,0,0)
##    e = time.time()
##    print 'fps:', fp/(e-s)
    print traceback.print_exc()
    
    
    
    
    
    
