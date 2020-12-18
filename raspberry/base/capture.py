import cv2
import numpy as np
import img
import picamera
import io
import time

HEIGHT = 240
WIDTH = 320
FPS = 80
BRIGHTNESS = 50
camera = picamera.PiCamera()
camera.resolution = (WIDTH,HEIGHT)
camera.framerate = FPS
camera.brightness = BRIGHTNESS
camera.shutter_speed = 1200
camera.exposure_mode = 'sports'
camera.ISO = 500
stream = io.BytesIO()

try:
        fp = 0
        s = time.time()
        for foo in camera.capture_continuous(stream,'jpeg',use_video_port=True):
                data = np.fromstring(stream.getvalue(),dtype=np.uint8)
                c_img = cv2.imdecode(data,cv2.CV_LOAD_IMAGE_UNCHANGED)
                cv2.imwrite('/home/pi/final/final_test/capture'+str(fp)+'.jpg',c_img)
##                cv2.imshow('c_img',c_img)
##                cv2.waitKey(30)
                print('done')
                fp += 1
                stream.truncate()
                stream.seek(0)
        camera.close()

##cap = cv2.VideoCapture(0)
##cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
##cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
##cap.set(cv2.cv.CV_CAP_PROP_FPS,80)

##thresh = 20
##try:
##    fp = 0
##    s = time.time()
##    while True:
##        ret,c_img = cap.read()
##        fp += 1
####        cv2.imwrite("/home/pi/code_by_yyt/capture5.jpg",frame)
##        cv2.imshow('c_img',c_img)
##        cv2.waitKey(10)

except :
    e = time.time()
    print(fp/(e-s))
    camera.close()
