#-*-coding:utf-8-*-
#code by yyt
#version1.0
    # 1.从文件夹中读取图像
    # 2.调整分辨率(shrink)
    # 3.提取红色部分(pick the red block)
    # 4.提取黑色部分(pick the blakc blokc)
    # 5.一阶矩获取中心点
#version1.1
    #加入了获取障碍物方位
#version1.2
    #封装成函数


import cv2
import numpy as np
import numpy
import time

####分辨率转换
##def shrink_img(img,height,width):
##    size = (width,height)
##    return cv2.resize(img,size,cv2.INTER_AREA)

##BRG转HSV
def change_hsv(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

##选取红色   
def red_bgr(img):
    redlower = np.array([0,0,130])
    redupper = np.array([110,100,255])
    return cv2.inRange(img,redlower,redupper)
    

##选取黑色
def pick_black(img):
    blacklower = np.array([0, 0, 9])
    blackupper = np.array([180, 255, 46])
    return cv2.inRange(img, blacklower, blackupper)

##二值化
#阈值thresh
#最大值max
def change_binary(img):
    ret, binary = cv2.threshold(img, 127, 255, 0)
    # ret1,binary = cv2.threshold(img,thresh,max,cv2.THRESH_BINARY)
    return binary

##求重心
def get_center(img):
    mymoment = cv2.moments(img,True)
    m00 = mymoment['m00']
    m10 = mymoment['m10']
    m01 = mymoment['m01']
    if m00 == 0:
        center = [-1,-1]
    else:
        middle_x = m10 / m00
        middle_y = m01 / m00
        center = [middle_x,middle_y]

    if ((center[1] > 100) and (m00<1000)):
        center = [-2,-2]
    return (center,m00)

##从原始图片到中心点
##def raw2center(img):
##    img = change_hsv(img)
##    img = red_bgr(img)
##    img = change_binary(img)
##    return get_center(img)
    
def counter_red(img):
    mymoment2 = cv2.moments(img,True)
    m001 = mymoment2['m00']
    return (m001/255)


def get_center_new(img):
    use_img = img
    bg = np.zeros_like(img)
##    print 'bg:',bg.shape,type(bg)
##    cv2.imshow('bg',bg)
##    cv2.waitKey(50)
    contours, some = cv2.findContours(use_img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
##    print('num of contours:',len(contours))
    if(len(contours) == 0):
        center = [-1,-1]
        m00 = 0
        xnz = [1000,1000]
        ynz = [1000,1000]
    else:
        max_area = 0
        max_index = 0
        index_num = 0
        for c_contour in contours:
                c_area = cv2.contourArea(c_contour)    
##                print(c_area)
                if(c_area > max_area):
                    max_area = c_area
                    max_index = index_num
                index_num += 1
##        print('max_index', max_index)
        cv2.drawContours(bg,contours,max_index,(255,255,255),2)
        ccc = np.nonzero(bg)
        xnz = ccc[1]
        ynz = ccc[0]
##        cv2.imshow('n_bg',bg)
##        cv2.waitKey(50)
        mymoment = cv2.moments(contours[max_index])
        m00 = mymoment['m00']
        m10 = mymoment['m10']
        m01 = mymoment['m01']
        if(m00 == 0):
            center = [-2,-2]
        else:
            middle_x = m10 / m00
            middle_y = m01 / m00
            center = [middle_x,middle_y]

##        if ((center[1] < 120) and (m00<1000)):
##            center = [-1,-1]
    dis_x_right = abs(center[0]-max(xnz))
    dis_x_left = abs(center[0]-min(xnz))
    dis_x_max = max(dis_x_right,dis_x_right)
    dis_y_up = abs(center[1]-max(ynz))
    dis_y_down = abs(center[1]-min(ynz))
    dis_y_max = max(dis_y_up,dis_y_down)
    
    dis_x = abs(dis_x_right - dis_x_left)
    dis_y = abs(dis_y_up - dis_y_down)
    dis_xy = abs(dis_x_max - dis_y_max)
    dis_max = max(dis_x,dis_y)
##    print 'center:',type(center)
##    print 'dis_x_max:',dis_x_max
##    print 'dis_y_max:',dis_y_max
##    print 'x:',dis_x
##    print 'y:',dis_y
##    print 'xy:',dis_xy
##    print 'dis_max:',dis_max
##    print 'm00:',m00
    return (center,m00,dis_xy,dis_x_right+dis_x_right)
    



def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
    try:
        fp = 0
        s = time.time()
        while True:
            ret,c_img = cap.read()
##            cv2.imshow('c_img',c_img)
##            cv2.waitKey(50)
            fp += 1
            c_red = red_bgr(c_img)
            c_red = change_binary(c_red)
####            cv2.imshow('c_red',c_red)
####            cv2.waitKey(10)
####            cv2.imwrite('/home/pi/final/final_test/white.jpg',c_img)
            center,red_num,dis_xy = get_center_new(c_red)
##            print 'center:',center
##            print 'red_num:',red_num
    finally:
        e = time.time()
        print 'fps:',(fp/(e-s))


def process_once():
    c_red = cv2.imread('/home/pi/final/final_test/cap1.jpg',0)
    c_red = change_binary(c_red)
    print c_red.shape
    cv2.imshow('c_red',c_red)
    cv2.waitKey(50)
    center,red_num = get_center_new(c_red)
        
    

if __name__ == "__main__":
    main()

##img = cv2.imread("g:/samples/test11.jpg")
##img = shrink_img(img,372,496)
# img = change_hsv(img)
# cv2.imshow('1',pick_red(img))
# cv2.waitKey()
# img = pick_red(img)
# img = change_binary(img)
# cv2.imshow('2',img)
# cv2.waitKey()
# center = get_center(img)
#print(raw2center(img))
# print(img.shape)
