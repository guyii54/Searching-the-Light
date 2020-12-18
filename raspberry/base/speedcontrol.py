# -*- coding: UTF-8 -*-
import time
import motor
import uart
import img
import cv2
import traceback

def standstill(speed,cs_thresh):   #保持静止
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
    SPEED = 0
    DIRECTION = 0
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
        #time.sleep(0.01)
##        if (abs(speedl - set_speed) >= 10):
        SPEED = (out_speed+speed_zero)
##            print("speedcontrol\n",SPEED)
##            print('out_speed:',out_speed)
        motor.set_car_run(1,SPEED,0)
##        else:
##            motor.set_car_run(1,set_speed,0)
##        else:
##            times += 1
##            if (times > 20):
        if (cs!=0) and (cs <cs_thresh):
            print 'cs1:',cs
            motor.set_car_run(1,0,0)
##            print times
##                motor.set_car_run(1,45,0)
            break
        #print(encoder.array[1],encoder.array[0])


        


##def stop():   #保持静止
##    speed_p = -190   #encoder and speed
##    speed_d = 25 
##    speed_i = 0
##    max_i_erro = 10
##    speed_zero = 0
##    set_speed = 0
##    last_value = 0
##    speed_i_erro = 0
##    SPEED = 0
##    DIRECTION = 0
##    times = 0
##    while True:
##        rf,speedl,speedr = uart.asksignal()
####        print speedl
##        if speedr == -1:
##            speedl = 0
##            speedr = 0
####        print (speedl,speedr)
##        c_speederro = speedr - set_speed
##        speed_i_erro += c_speederro*0.01
##        speed_i_erro = motor.limiter(speed_i_erro,-max_i_erro,max_i_erro)
##        l_speederro = last_value - set_speed
##        out_speed = speed_p*c_speederro+speed_d*l_speederro+speed_i*speed_i_erro
##        last_value = speedr
##        #time.sleep(0.01)
##        if (speedr != 0):
##            SPEED = (out_speed+speed_zero)
##               #print("speedcontrol\n",SPEED)
####            print('out_speed:',out_speed)
##            motor.set_car_run(1,SPEED,DIRECTION)
##        else:
##            times += 1
####            if (times > 1000):
####                motor.set_car_run(1,45,0)
####                break


def cs_stop():   #保持静止
##    uart.startcs()
##    time.sleep(0.01)
    speed_p = -70   #encoder and speed
    speed_d = 0 
    speed_i = 0
    max_i_erro = 10
    speed_zero = 0
    set_speed = 0
    last_value = 0
    speed_i_erro = 0
    SPEED = 0
    DIRECTION = 0
    times = 0
    
##    while True:
##        cs,speedl,speedr = uart.askcs()
####        print cs
##        if ((cs != 0) and (cs <cs_thresh)):
##            print cs
##            break
##    print 'stop now'
    while True:
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
        #time.sleep(0.01)
        if (speedr != 0):
            SPEED = (out_speed+speed_zero)
               #print("speedcontrol\n",SPEED)
##            print('out_speed:',out_speed)
            motor.set_car_run(1,SPEED,DIRECTION)
        else:
            motor.set_car_run(1,0,0)
            if ((cs!=0) and(cs < 1350)):
    ####            times += 1
    ####            if (times > 10000):
                print 'cs2',cs
                uart.endcs()
                break

            
    
def wheelstop():   
    direct_p = -90   
    direct_d = 0 
    direct_i = 0
    max_i_erro = 10
    speed_zero = 0
    set_speed = 0
    speed = 0
    last_value = 0
    direct_i_erro = 0
##    still_flag = 1
    SPEED = 0
    DIRECTION = 0
    num = 0
    while True:
        rf,speedl,speedr = uart.asksignal()
        if speedr == -1:
            speedl = 0
            speedr = 0
##        print (speedl,speedr)
        c_directerro = (speedl-speedr) - set_speed
        direct_i_erro += c_directerro*0.01
        direct_i_erro = motor.limiter(direct_i_erro,-max_i_erro,max_i_erro)
        l_directerro = last_value 
        out_direct = direct_p*c_directerro+direct_d*l_directerro+direct_i*direct_i_erro
        last_value = speedl-speedr
        #time.sleep(0.01)
        if ((abs(speedl-speedr))>10):
            direct = out_direct
##            SPEED = (out_speed+speed_zero)
               #print("speedcontrol\n",SPEED)
##            print('out_speed:',out_speed)
            motor.set_car_run(1,speed,out_direct)
        else:
            motor.set_car_run(1,0,0)
            num += 1
            if (num >= 3):
                break
##            direct = 0
##            motor.set_car_run(1,0,0)
##            break
        #print (speedl,speedr,direct)

        
        

def speedcontrol_test():
    motor.init_motor(500)
    motor.stop()
##    motor.set_car_run(1,100,0)
##    time.sleep(4)
    standstill(15,1000)
##    time.sleep(0.5)
##    print 'stop'
##    while True:
##        motor.set_car_run(1,45,0)

##    HEIGHT = 240
##    WIDTH = 320
##    speed = 150
##    DIRECTION = 0
##    k_img_direct = 0.5
##    dis_thresh = 170
##    st2_direct_limmiter = 130
##
##    cap = cv2.VideoCapture(0)
##    cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
##    cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
##
##    motor.init_motor(500)
##    motor.stop()
##    
##    while True:
##        ret,c_img = cap.read()
##        c_red = img.red_bgr(c_img)
##        c_red = img.change_binary(c_red)
##        c_center,red_num,dis_xy = img.get_center_new(c_red)
##        direct = k_img_direct * (c_center[0]-((WIDTH/2)+30))
##        direct = motor.limiter(direct,-st2_direct_limmiter,st2_direct_limmiter)
####        print (direct)
##        motor.set_car_run(1,speed,direct)
####        print (c_center)
##        if (c_center[1] >= HEIGHT-dis_thresh):
##            break
        

def main():
    speedcontrol_test()
    #keep_speed()
    
    
if __name__ == "__main__":
    try:
        speedcontrol_test()
    finally:
        motor.set_car_run(1,0,0)
##        process_count_thread.stop()
##        process_timer.stop()
##        thread_motor.stop()
##        thread_standstill.stop()
##        GPIO.cleanup();
        print (traceback.print_exc())
        
    

    
