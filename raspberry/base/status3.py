import time
import picamera
import cv2
import io
import numpy as np
import img
import matplotlib.pyplot as plt
import motor

#***********global values***********
status = 3
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

#*********initial motor*************


#*********initial encoder**********


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
camera.sleep(1)
stream = io.BytesIO()


for foo in camera.capture_continuous(stream,'jpeg',use_video_port=True):
	data = np.fromstring(stream.getvalue(),dtype=np.uint8)
	c_img = cv2.imdecode(data,cv2.CV_LOAD_IMAGE_UNCHANGED)
	
	if(status == 3):
		if(real_speed == 0):
			status = 4
		else:
			status = 3
			
	print('current status:%d' % status)
	
	if(status == 3)
		motor.stop()
		real_speed = encoder.readmotor()
		print('real_speed:%d' % real_speed)
		
	else:
		print('done')
		break







