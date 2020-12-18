import time
import picamera
import cv2
import io
import numpy as np
import img
import matplotlib.pyplot as plt
import motor
from multiprocessing import Process,Value
import speedcontrol
import encoder

status = 2
speed= 0
direct = 0
	#direct >0,turn left
bias_thresh = 7
	#when in status1 c_center[0] and WIDTH/2's distance <= bias_thresh,change into status2
dis_thresh = 100
	#when in status2 c_center[1] <= HEIGHT-dis_thresh,chan into status3
l_center = 0
	
#*******status1 values
comfirm_get = 200
wh_direct = 20

#******status2 values
st2_speed = 60
l1_direct = 40
l2_direct = 20
r1_direct = -40
r2_direct = -20
ob_thresh = 20
	#if black pixel's number >= ob_thresh,see is as there is obstacle
st2_flag = 0
	#whether there are obstacle,1 means yes

#******status3 values
real_speed = 0

#******status4 values
rednumber_thresh = 200
	#when in status4 rednumber <= 200,it means there no red any more,change into status1
st4_flag = 0
	#whether the arm has been in,1 means it has been
getin_num = 0
	#how many time has function helm.getin() been used
getin_num_thresh = 10


#*********initial camera***********
HEIGHT = 240
WIDTH = 320
FPS = 40
BRIGHTNESS = 50
camera = picamera.PiCamera()
camera.resolution = (WIDTH,HEIGHT)
camera.framerate = FPS
camera.brightness = BRIGHTNESS
# camera.shutter_speed = 5000000
camera.exposure_mode = 'auto'
camera.ISO =200
#camera.sleep(1)
stream = io.BytesIO()
try:
        for foo in camera.capture_continuous(stream,'jpeg',use_video_port=True):
                data = np.fromstring(stream.getvalue(),dtype=np.uint8)
                c_img = cv2.imdecode(data,cv2.CV_LOAD_IMAGE_UNCHANGED)
                
                if(status == 2):
                        # red = img.change_hsv(c_img)
                        # red = pick_red(red)
                        # cv2.imshow('red',red)
                        # cv2.waitKey(10)
                        c_center = img.raw2center(c_img)
                        if(c_center[1] >= HEIGHT-dis_thresh):
                                status = 3
                        else:
                                status = 2
                                
                else:
                        print('status:%d' % status)
                        print('status3,center:',c_center)
finally:
        camera.close()
##		
##	
##	if(status ==2):
##		speed = st2_speed
##		obs = obstacle.get_ob_dir(c_img,ob_thresh)
##		if((obs[0]+obs[1]+obs[2]+obs[3])==0):
##			st2_flag = 0
##		else:
##			st2_flag = 1
##			
##		if(st2_flag==0):
##			if(img.counter_red(img) > comfirm_get):
##				direct =motor.cut_bias(c_center,l_center,WIDTH)
##			else:
##				temp_direct = -direct
##				direct = temp_direct
##		else:
##			if(obs[0]==1):
##				direct = r2_direct
##			elif(obs[3]==1):
##				direct = l2_direct
##			elif(obs[2]==1):
##				direct = l1_direct
##			elif(obs[1]==1):
##				direct = r1_direct
##			else:
##				direct = 0
##		l_center = c_center
##		print('status2:direct set:%d' %direct)
##		motor.set(speed,direct)
##		
##	else:
##		print('status:%d' % status)
##		print("status3,c_center:%d"%c_center)
##		print('done')
##		break





##global still_flag
##still_flag = 1
##motor.init_motor(500)
##encoder.start_encoder()
##motor.stop()
##'''
##print('done')
##speed = 100
##direct = 0
##motor.set_car_run(1,speed,direct)
##time.sleep(3)
##print('here')
##'''
###motor.set_car_run(0,0,0)
##print("OK")
###standstill_thread = thread.threading(target = speedcontrol.standstill, args = ())
##speedcontrol.standstill()
##
##time.sleep(1)
##speedcontrol.still_flag = 0
###motor.set_car_run(0,0,0)
