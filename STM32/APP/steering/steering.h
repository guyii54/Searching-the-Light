#ifndef _steering_H
#define _steering_H
#include "stm32f10x.h"

#define steering_pin GPIO_Pin_5	//PB5

void steering_init(void);//�����ʼ��
void steering_chg(uint16_t angle);	//��������
void steering_out(void);		//������
void steering_in(void);		//�ջض��
void steering_out_in(void);	//�������ջغ���

#endif
