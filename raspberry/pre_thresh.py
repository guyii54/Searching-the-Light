#-*-coding:utf-8-*-
import cv2
import numpy as np
import img
import picamera
import io
import time
import traceback
##import obstacle


HEIGHT = 240
WIDTH = 320
FPS = 80
BRIGHTNESS = 50
##camera = picamera.PiCamera()
##camera.resolution = (WIDTH,HEIGHT)
##camera.framerate = FPS
##camera.brightness = BRIGHTNESS
##camera.shutter_speed = 800   #us
##camera.exposure_compensation = 25
####camera.exposure_mode = 'auto'
##camera.ISO = 1200
##camera.exposure_mode = 'sports'
##
##stream = io.BytesIO()

cap = cv2.VideoCapture(0)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, HEIGHT)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, WIDTH)
##cap.set(cv2.cv.CV_CAP_PROP_FPS,80)

def nothing(x):
    pass
    



pre_bmax,pre_gmax,pre_rmax = [110,110,255]
pre_bmin,pre_gmin,pre_rmin = [0,0,120]


#**********************adjust black thresh*************
cv2.namedWindow('pick_black',1)
cv2.createTrackbar('bmax','pick_black',pre_bmax,255,nothing)
cv2.createTrackbar('rmax','pick_black',pre_rmax,255,nothing)
cv2.createTrackbar('gmax','pick_black',pre_gmax,255,nothing)
cv2.createTrackbar('bmin','pick_black',pre_bmin,255,nothing)
cv2.createTrackbar('rmin','pick_black',pre_rmin,255,nothing)
cv2.createTrackbar('gmin','pick_black',pre_gmin,255,nothing)

# c_img = cv2.imread(r'D:\code_by_yyt\proj\near.jpg')
# hsv = img.change_hsv(c_img)
try:
    fp = 0
    s = time.time()
##    for foo in camera.capture_continuous(stream,'jpeg',use_video_port=True):
##        data = np.fromstring(stream.getvalue(),dtype=np.uint8)
##        c_img = cv2.imdecode(data,cv2.CV_LOAD_IMAGE_UNCHANGED)
    while True:
        ret,c_img = cap.read()
        fp += 1
        cv2.imshow('c_img',c_img)
        cv2.waitKey(10)
        fp += 1
        bmax = cv2.getTrackbarPos('bmax','pick_black')
        rmax = cv2.getTrackbarPos('rmax','pick_black')
        gmax = cv2.getTrackbarPos('gmax','pick_black')
        bmin = cv2.getTrackbarPos('bmin','pick_black')
        rmin = cv2.getTrackbarPos('rmin','pick_black')
        gmin = cv2.getTrackbarPos('gmin','pick_black')
        
        
        redlow = np.array([bmin,gmin,rmin])
        redupp = np.array([bmax,gmax,rmax])
        
        c_red = cv2.inRange(c_img,redlow,redupp)
        cv2.imshow('pick_black',c_red)
        k = cv2.waitKey(10)
        c_red = img.change_binary(c_red)
        c_center,red_num,dis_xy ,dis_x= img.get_center_new(c_red)
        print 'center:',c_center,dis_x,red_num
        
##        stream.truncate()
##        stream.seek(0)


except :
    e = time.time()
##    camera.close()
    print('fps:',fp/(e-s))
    print traceback.print_exc()
    
##cv2.destroyAllWindows()








