#-*-coding:utf-8-*-
#code by yyt
#version_beta
    #1.寻找1,2,3,4区域是否有障碍
    #2.判断是否有障碍方法：对一块区域求黑色像素点个数
    #3.get_ob_dir函数



import numpy
import cv2
import numpy as np
import time
import pandas as pd
##取数组并对像素点求和
##para:
    #beginline,beginrow:开始行，开始列
    #height,width:总行数，列数
    #ROI = img[beginline:beginline+height,beginrow:beginrow+width]
	
def pick_roi(img,ROIset):
	return img[ROIset[0]:ROIset[0]+ROIset[2],ROIset[1]:ROIset[1]+ROIset[3]]
	
	
	
def pick_and_sum(img,ROIx):
	ROI = img[ROIx[0]:ROIx[0]+ROIx[2],ROIx[1]:ROIx[1]+ROIx[3]]
	sum255 = np.sum(ROI)
	sum = sum255/255
	#print(ROI)
	return sum

##导出数据到excel表格
def export_to_excel(img,path):
	data_df = pd.DataFrame(img)
	# print(type(data_df))
	writer = pd.ExcelWriter(path)
	data_df.to_excel(writer,'page_1')
	writer.save()
	return

##判断1,2,3,4方向是否有障碍,
def get_ob_dir(img,thresh):
	obstacle = [0,0]
	ROI0 = [120,0,25,110]
	ROI1 = [80,81,25,110]
	ROI2 = [80,161,25,80]
	ROI3 = [120,240,25,80]
	obs = [0,0,0,0]
	if pick_and_sum(img,ROI0) >= thresh:
		obs[0] = 1
	if pick_and_sum(img,ROI1) >= thresh:
		obs[1] = 1
	if pick_and_sum(img,ROI2) >= thresh:
		obs[2] = 1
	if pick_and_sum(img,ROI3) >= thresh:
		obs[3] = 1
	return four_way




# test
# b = np.array([[1,2,3],[1,3,4]])
# sum1 = np.sum(b)
# print b.shape

# img = cv2.imread("g:/samples/test11.jpg")
# img = find_the_light_function_v1d2.shrink_img(img,240,320)
# #print(img)
# img = find_the_light_function_v1d2.change_hsv(img)
# img = find_the_light_function_v1d2.pick_black(img)
# img = find_the_light_function_v1d2.change_binary(img)
# cv2.imshow("show",img)
# cv2.waitKey()
# start = time.clock()
# # export_to_excel(img,'g:/samples/xlsx.xlsx')
# thresh = 20
# ret = get_ob_dir(img,thresh)
# end = time.clock()
# print(ret)
# print(end-start)
