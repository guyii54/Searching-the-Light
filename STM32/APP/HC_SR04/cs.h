#ifndef _CS_H
#define _CS_H


#include "stm32f10x.h"
#define uint unsigned int
#define pin_cs_trig GPIO_Pin_14			//触发信号PB14
#define pin_cs_echo GPIO_Pin_15			//接收信号PB15
#define TRIG_Send  GPIO_SetBits(GPIOB,pin_cs)
#define ECHO_Reci  GPIO_ReadInputDataBit(GPIOB,GPIO_Pin_9)

void ch_sr04_init(void);
float Senor_Using(void);
void NVIC_Config(void);

#endif
