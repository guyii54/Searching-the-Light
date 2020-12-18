import time
import picamera
import cv2
import io
import numpy as np
import img
import matplotlib.pyplot as plt
import motor

status = 1
speed= 0
direct = 0
mode = -1
l_center = 0

    #direct >0,turn left
bias_thresh = 7
    #when in status1 c_center[0] and WIDTH/2's distance <= bias_thresh,change into status2
dis_thresh = 100
    #when in status2 c_center[1] <= HEIGHT-dis_thresh,chan into status3

#*******status1 values
comfirm_get = 100
wh_direct = 20

#*********initial camera***********
HEIGHT = 240
WIDTH = 320
FPS = 40
BRIGHTNESS = 50
camera = picamera.PiCamera()
camera.resolution = (WIDTH,HEIGHT)
##camera.framerate = FPS
camera.brightness = BRIGHTNESS
camera.shutter_speed = 500000
camera.exposure_mode = 'auto'
camera.ISO = 500
camera.awb_mode = 'fluorescent'

stream = io.BytesIO()


#*********initial motor*************
motor.init_motor(500)



for foo in camera.capture_continuous(stream,'jpeg',use_video_port=True):
    data = np.fromstring(stream.getvalue(),dtype=np.uint8)
    c_img = cv2.imdecode(data,cv2.CV_LOAD_IMAGE_UNCHANGED)
    cv2.imshow('c_img',c_img)
    cv2.waitKey(10)
    
    if(status==1):
##        hsv = img.change_hsv(c_img)
        c_red = img.red_bgr(c_img)
        c_red = img.change_binary(c_red)
        c_center,num = img.get_center(c_red)
        cv2.imshow('c_red',c_red)
        cv2.waitKey(10)
        print('num')
        print(num)
        #print(c_center)
##        print('counter')
##        print(img.counter_red(c_img))
##        print('c_center:')
##        print(c_center)
        #c_center means center of the red block now
        if((num > comfirm_get) and (abs(c_center[0]-WIDTH/2) <= bias_thresh)):
            status = 2
##            print('counter')
##            print(img.counter_red(c_img))
        else:
##            print('counter')
##            print(img.counter_red(c_img))
            status = 1
    
    if(status == 1):
##        print('status1,c_center:')
##        print(c_center)
        if(img.counter_red(c_red) > comfirm_get):
            direct = motor.cut_bias(c_center,l_center,WIDTH)
        else:
            direct = wh_direct
        l_center = c_center
        #remain
        print('direct')
        print(direct)
##        cv2.imshow('red',c_red)
##        cv2.waitKey(10)
##        motor.set(speed,direct)
        
    else:
        print('status2,c_center:')
        print(c_center)
        print('done')
        break
    
    stream.truncate()
    stream.seek(0)
    
    
    
    
    
    
