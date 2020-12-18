# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

BEEP_PIN = 4



def initial_beep():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(BEEP_PIN,GPIO.OUT)


def beep_on():
    GPIO.output(BEEP_PIN,0)
    

def beep_off():
    GPIO.output(BEEP_PIN,1)

def beep_once():
    beep_on()
    time.sleep(0.5)
    beep_off()

def beep_warning():
    i = 0
    beep_on()
    time.sleep(1)
    beep_off()


def main():
    initial_beep()
    time.sleep(0.5)
    beep_done()
    

if __name__ == "__main__":
    main()

