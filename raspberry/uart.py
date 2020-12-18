## # -*- coding: utf-8 -*
import serial
import time
import traceback
ser = serial.Serial("/dev/ttyAMA0", 115200)
print ser.port
print ser.baudrate


def ask():
    try:
        fp = 0
        sum_r = 0
##        s = time.time()
        while True:
            ser.write('send')
            count = ser.inWaiting()
            if count != 0:
                recv = ser.read(14)
                print recv
                fp +=1
    ##            recv = int(recv)    #stm32以16位的无符号数传入，但树莓派自动将其转为了字符类  
    ##            print recv
            ser.flushInput()
            time.sleep(0.1)
    except:
        if ser != None:
            ser.close()
##        e = time.time()
##        print (fp/(e-s))
##        print e-s
        
##        print 'done once'
##        count = ser.inWaiting() 
##        if count != 0:
##            print 'count:',count
##            recv = ser.read(5)
##            print recv
##            ser.write(recv)
##        ser.flushInput()
##        time.sleep(0.1)

def asksignal():
    ret = 0
    ser.write('s12d')
##    print '2'
    time.sleep(0.01)
    count = ser.inWaiting()
    if count != 0:
        frame = ser.read(14)
##    print count
    
##    print frame
##    print frame
    
        rfi = frame[0:4]
        rf = [int(rfi[0]),int(rfi[1]),int(rfi[2]),int(rfi[3])]
    
        speedl = frame[5:9]
        speedr = frame[10:14]
        speedr = int(speedr)
        speedl = int(speedl)
##    ser.close()
##    print rfi
##    print speedl
    else:
        rf = [-1,-1,-1,-1]
        speedl = -1
        speedr = -1
    ser.flushInput()
    ret = 1
    
    return rf, speedl, speedr

def askcs():
    ret = 0
    ser.write('s12345d')
    time.sleep(0.01)
    count = ser.inWaiting() 
    if count != 0:
        frame = ser.read(15)
##        print frame
        cs = frame[0:5]
        cs = int(cs)
        speedl = frame[6:10]
        speedr = frame[11:15]
        speedl = int(speedl)
        speedr = int(speedr)
    else:
        cs = -1
        speedl = -1
        speedr = -1
    ser.flushInput()
    
    return cs,speedl,speedr

def startcs():
    ser.write('s1d')

def endcs():
    ser.write('s123d')

def usehelm():
    ser.write('s123456d')
##    print 'write done'
    

def main():
    try:
        ret = 0
        s= time.time()
        fp = 0
##        usehelm()
        startcs()
        while True:
##            rf,speedl,speedr = asksignal()
            cs ,speedl,speedr = askcs()
##            ask()
##            fp += 1
    ##        print type(cs)
##            print rf,speedl,speedr
            print 'cs:',cs,speedl,speedr
    finally:
        e = time.time()
        print fp/(e-s)
        endcs()
        
                
            
        

if __name__ == '__main__':
    try:
        main()
    except :
        if ser != None:
            ser.close()
        print traceback.print_exc()
        endcs()
