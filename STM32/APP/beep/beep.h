#ifndef _BEEP_H
#define _BEEP_H
#include "stm32f10x.h"
#define BEEP_Pin GPIO_Pin_1

void BEEP_Init(void);			//��������ʼ������
void beep_change(void);		//�ı������״̬
void beep_off(void);			//��������
void beep_on_ms(int time);						//�������죬�趨ʱ��time(ms)
void beep_on_us(int time);							//�������죬�趨ʱ��time(us)

#endif
