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

status = 1
speed= 0
direct = 0
mode = -1
l_center = 0

    #direct >0,turn left
bias_thresh = 70
    #when in status1 c_center[0] and WIDTH/2's distance <= bias_thresh,change into status2
dis_thresh = 30
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

motor.car_run_flag = 1
try:
    fp = 0
    #motor.set_car_run(1,0,150)
    #time.sleep(5)
    s = time.time()
    for foo in camera.capture_continuous(stream,'jpeg',use_video_port=True):
##        s = time.time()
        data = np.fromstring(stream.getvalue(),dtype=np.uint8)
        c_img = cv2.imdecode(data,cv2.CV_LOAD_IMAGE_UNCHANGED)
##        cv2.imwrite('/home/pi/final/final_test/capture'+str(fp)+'.jpg',c_img)

        
        fp+=1
##        cv2.imshow('c_img',c_img)
##        cv2.waitKey(10)

        if(status==1):
            c_red = img.red_bgr(c_img)
            c_red = img.change_binary(c_red)
            c_center,red_num = img.get_center(c_red)
            cv2.imshow('c_red',c_red)
            cv2.waitKey(10)
            #print('num')
##            print(num,encoder.array[:])
            print 'red_number:',red_num
            print 'center:',c_center
            
            if ((red_num > comfirm_get) and (abs(c_center[0] - WIDTH/2) < bias_thresh)):
                status = 2
                #停止电机
                #speedcontrol.stop_now('direct')
                print('stop done')  
                motor.set_car_run(0,0,0)
            #当红点数大于阈值且灯重心距离足够近


        
        if(status == 1):
            direct = wh_direct
            speed = 0
            #motor.set_car_run(1,speed,direct)
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
            c_center = img.raw2center(c_img)
            print("statues2:")
            if(c_center[0][1] >= HEIGHT-dis_thresh):
                status = 3
                print("2 to 3")
                break
            else:
                status = 2
    
        stream.truncate()
        stream.seek(0)
##        e= time.time()
##        print(e-s)

    e= time.time()
    camera.close()
    print (fp/(e-s))

except:
    camera.close()
    motor.set_car_run(0,0,0)
##    e = time.time()
##    print 'fps:', fp/(e-s)
    print traceback.print_exc()
    
    
    
    
    
    
