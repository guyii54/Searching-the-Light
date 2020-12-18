import cv2
import numpy as np
import io
import picamera
import time
import motor
import speedcontrol
import encoder
import traceback

motor.init_motor(500)
motor.stop()
encoder.start_encoder()

try:
        speed = 0
        direct = 130
        motor.set_car_run(1,speed,direct)
        time.sleep(10)
        print encoder.array[:]
        if(speedcontrol.stop_now('direct') == 1):
                print('stop done')
        motor.set_car_run(1,0,0)

except:
        motor.set_car_run(0,0,0)
        print 'error'
        print traceback.print_exc()





