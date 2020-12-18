# -*- coding: UTF-8 -*-
import RPi.GPIO as GPIO
import time
import threading

##define BCM
#left motor
M1 = 20
M2 = 21
PWMA = 26
#right motor
M3 = 6
M4 = 13
PWMB = 12
#hongwai
IR_PIN = 18

##global values
global PWM_MAX
global PWM_MIN
global DIR_MAX
global DIR_MIN
global MAX_SPEED
global MAX_DIRECTION
global p1
global p2
global LEFT_K
global RIGHT_K
global gl_IR_temp
LEFT_K = 1.0
RIGHT_K = 1.0
PWM_MAX = 40
PWM_MIN = 2
DIR_MAX = 20
DIR_MIN = -20
MAX_SPEED = 250
MAX_DIRECTION = 200
gl_IR_temp = 20
##initial motor with duty cycle
def init_motor(cycle):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(M1,GPIO.OUT)
    GPIO.setup(M2,GPIO.OUT)
    GPIO.setup(M3,GPIO.OUT)
    GPIO.setup(M4,GPIO.OUT)
    GPIO.setup(PWMA,GPIO.OUT)
    GPIO.setup(PWMB,GPIO.OUT)
    
    global p1
    global p2
    p1 = GPIO.PWM(PWMA,500) #left motor
    p2 = GPIO.PWM(PWMB,500) #right motor
    p1.start(50)    #占空比50%
    p2.start(50)

def init_IR():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(IR_PIN,GPIO.IN,GPIO.PUD_UP)
    
def set_motor(A1,A2,B1,B2): 
    GPIO.output(M1,A1)
    GPIO.output(M2,A2)
    GPIO.output(M3,B1)
    GPIO.output(M4,B2)

def forward():
    set_motor(1,0,0,1)
def stop():
    set_motor(0,0,0,0)
def circle():
    set_motor(0,1,0,1)
def backward():
    set_motor(0,1,1,0)
def turn_left():
    set_motor(0,0,0,1)
def turn_right():
    set_motor(1,0,0,0)
def left_back():
    set_motor(0,1,0,0)
def right_back():
    set_motor(0,0,1,0)

def limiter(data,MIN,MAX):
    if data <= MIN:
        data = MIN
    elif data >= MAX:
        data = MAX
    return data

def set_motor_speed(MOTOR,speed):
    global LEFT_K
    global RIGHT_K
    speed /= 5
    if MOTOR == 1:
        speed *= LEFT_K
        if speed > 0:
            GPIO.output(M1,0)
            GPIO.output(M2,1)
            p1.ChangeDutyCycle(speed)
        elif speed < 0:
            GPIO.output(M1,1)
            GPIO.output(M2,0)            
            p1.ChangeDutyCycle(-speed)
        else:
            GPIO.output(M1,0)
            GPIO.output(M2,1)
            p1.ChangeDutyCycle(0)
    elif MOTOR == 0:
        speed *= RIGHT_K
        if speed > 0:
            GPIO.output(M3,1)
            GPIO.output(M4,0)
            p2.ChangeDutyCycle(speed)
        elif speed < 0:
            GPIO.output(M3,0)
            GPIO.output(M4,1)            
            p2.ChangeDutyCycle(-speed)
        else:
            GPIO.output(M3,1)
            GPIO.output(M4,0)
            p2.ChangeDutyCycle(0)

def set_car_run(car_run_flag,speed,direction):
    speed = limiter(speed,-MAX_SPEED,MAX_SPEED)
    direction = limiter(direction,-MAX_DIRECTION,MAX_DIRECTION)
    if car_run_flag == 1:
        set_motor_speed(0,speed+direction)
        set_motor_speed(1,speed-direction)
    if car_run_flag ==0:
        set_motor_speed(0,0)
        set_motor_speed(1,0)



def run_motor(motor_mode,PWM,DIR):
    if motor_mode == 0:
        stop()
    elif motor_mode == 1:
        forward()
    elif motor_mode == 2:
        backward()
    elif motor_mode == 3:
        turn_left()
    elif motor_mode == 4:
        turn_right()
    elif motor_mode == 5:
        circle()    
    elif motor_mode == 6:
        left_back()
    elif motor_mode == 7:
        right_back()
        
    global p1
    global p2
    p1.ChangeDutyCycle(limiter(PWM+DIR,PWM_MIN,PWM_MAX))
    p2.ChangeDutyCycle(limiter(PWM-DIR,PWM_MIN,PWM_MAX))

def powerout(pwm):
    global p1
    global p2
    p1.ChangeDutyCycle(limiter(PWM-DIR,PWM_MIN,PWM_MAX))
    p2.ChangeDutyCycle(limiter(PWM+DIR,PWM_MIN,PWM_MAX))
    
def key_control():
    global PWM
    global DIR
    global MODE
    #while True:
    temp = raw_input("input wsad m to change state\n")
    if temp == 'm':
        p1.start(50)    #占空比50%
        p2.start(50)        
        MODE += 1
        if MODE > 7:
            MODE = 1
    elif temp == 'w':
        #PWM += 1
        PWM = 15
        DIR = 0
    elif temp == 's':
        #PWM -= 1
        PWM = 0
        DIR = 0
    elif temp == 'a':
        #DIR -= 1
        DIR =-5
    elif temp == 'd':
        #DIR += 1
        DIR = 5
    elif temp == 'p':
        p1.stop()
        p2.stop()
    elif temp == 'j':
        PWM += 2
    elif temp == 'k':
        PWM += 2
    else:
        stop()
    #time.sleep(0.5)

#hongwai
def getkey():
    if GPIO.input(IR_PIN) == 0:
        count = 0
        while GPIO.input(IR_PIN) == 0 and count < 200:  #9ms
            count += 1
            time.sleep(0.00006)
        count = 0
        while GPIO.input(IR_PIN) == 1 and count < 80:  #4.5ms
            count += 1
            time.sleep(0.00006)
        idx = 0
        cnt = 0
        data = [0,0,0,0]
        for i in range(0,32):
            count = 0
            while GPIO.input(IR_PIN) == 0 and count < 15:    #0.56ms
                count += 1
                time.sleep(0.00006)			
            count = 0
            while GPIO.input(IR_PIN) == 1 and count < 40:   #0: 0.56ms
                count += 1                               #1: 1.69ms
                time.sleep(0.00006)		
            if count > 8:
                data[idx] |= 1<<cnt
            if cnt == 7:
                cnt = 0
                idx += 1
            else:
                cnt += 1
        if data[0]+data[1] == 0xFF and data[2]+data[3] == 0xFF:  #check
            return data[2]

def show_IRKey():
    init_IR()
    while True:
        key = getkey()
        if(key != None):
            print("Get the key: 0x%02x" %key)

def IR_control():
    global SPEED
    global DIRECTION
    global gl_IR_temp
    CON_SPEED = 70
    CON_DIRECTION = gl_IR_temp
    init_IR()
    IR_flag = 1
    while IR_flag == 1:
        key = getkey()
        if(key != None):
            #print("Get the key: 0x%02x" %key)
            if key == 0x02:
                set_car_run(1,2*CON_SPEED,0)
                time.sleep(0.5)
                SPEED = CON_SPEED
                DIRECTION = 0
                print("forward")
            if key == 0x04:
                SPEED = CON_SPEED
                DIRECTION = -CON_DIRECTION
                print("left")
            if key == 0x12:
                SPEED = 0
                DIRECTION = 0
                print("stop")
            if key == 0x06:
                SPEED = CON_SPEED
                DIRECTION = CON_DIRECTION
                print("right")
            if key == 0x08:
                SPEED = -CON_SPEED
                DIRECTION = 0	
                print("reverse")
            if key == 0x1a:
                if(SPEED + 10 < MAX_SPEED):
                    SPEED = SPEED + 10
                    print(SPEED)
            if key == 0x1e:
                if(SPEED - 10 > -1):
                    SPEED = SPEED - 10
                    print(SPEED)
            if key == 0x1b:
                gl_IR_temp +=5	
                print("CON_DIRECTION+5")
            if key == 0x1f:
                gl_IR_temp -=5	
                print("CON_DIRECTION-5")
            IR_flag = 0

def test_motor():
    global MODE
    global PWM
    global DIR
    global SPEED
    global DIRECTION
    MODE = 0    
    PWM = 0
    DIR = 0
    SPEED = 0
    DIRECTION = 0

    init_motor(500)
    stop()
    try:
        while True:
            IR_control()
            #key_control()
            #time.sleep(0.01)
            #run_motor(MODE,PWM,DIR)
            set_car_run(1,SPEED,DIRECTION)
            
    finally:
        GPIO.cleanup();

def main():
    test_motor()
    #show_IRKey()


if __name__ == "__main__":
    main()
    
