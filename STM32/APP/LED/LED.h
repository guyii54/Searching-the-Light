#ifndef _LED_H
#define _LED_H
#include "stm32f10x.h"
#define LED_Pin GPIO_Pin_1	//PA1

void LED_Init(void);	//LED��ʼ������
void LED_Display();	//LED��˸
void LED_OFF();	//LED�ر�
void LED_ON();		//LED��
void LED_Change();	//LED�ı�״̬
void LED_Rxsuccess();	//UART�н��ճɹ���˸
void LED_Rxfail();		//UART�н���ʧ����˸

#endif
