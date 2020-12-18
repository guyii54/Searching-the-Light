#ifndef _exti_H
#define _exti_H
#include "stm32f10x.h"
#define K_1 GPIO_Pin_0 //PB0 按键

/*
#define K_2 GPIO_Pin_1
#define K_3 GPIO_Pin_2
#define K_4 GPIO_Pin_3
#define K_5 GPIO_Pin_4
#define K_6 GPIO_Pin_5
#define K_7 GPIO_Pin_6
#define K_8 GPIO_Pin_7
*/


void exti_init(void);	//外部中断0初始化



#endif
