#ifndef _LED_H
#define _LED_H
#include "stm32f10x.h"
#define LED_Pin GPIO_Pin_1	//PA1

void LED_Init(void);	//LED初始化函数
void LED_Display();	//LED闪烁
void LED_OFF();	//LED关闭
void LED_ON();		//LED打开
void LED_Change();	//LED改变状态
void LED_Rxsuccess();	//UART中接收成功闪烁
void LED_Rxfail();		//UART中接收失败闪烁

#endif
