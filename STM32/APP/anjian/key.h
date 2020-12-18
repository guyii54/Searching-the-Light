#ifndef _key_H
#define _key_H
#include "stm32f10x.h"
#define K_1 GPIO_Pin_0
#define K_2 GPIO_Pin_1
#define K_3 GPIO_Pin_2
#define K_4 GPIO_Pin_3
#define K_5 GPIO_Pin_5
#define K_6 GPIO_Pin_6
#define K_7 GPIO_Pin_7
#define K_8 GPIO_Pin_8

//#define k_1 GPIO_ReadInputDataBit(GPIOA,K_1)
#define k_2 GPIO_ReadInputDataBit(GPIOA,K_2)
#define k_3 GPIO_ReadInputDataBit(GPIOA,K_3)
#define k_4 GPIO_ReadInputDataBit(GPIOA,K_4)

void key_init(void);


#endif
