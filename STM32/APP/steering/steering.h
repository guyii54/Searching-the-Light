#ifndef _steering_H
#define _steering_H
#include "stm32f10x.h"

#define steering_pin GPIO_Pin_5	//PB5

void steering_init(void);//舵机初始化
void steering_chg(uint16_t angle);	//给定脉宽
void steering_out(void);		//伸出舵机
void steering_in(void);		//收回舵机
void steering_out_in(void);	//舵机伸出收回函数

#endif
