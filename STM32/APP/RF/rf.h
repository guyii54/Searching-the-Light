#ifndef _RF_H
#define _RF_H
#include "stm32f10x.h"
#define RF_fl_Pin GPIO_Pin_8	//PB8
#define RF_sl_Pin GPIO_Pin_11	//PB11
#define RF_fr_Pin GPIO_Pin_12	//PB12
#define RF_sr_Pin GPIO_Pin_14	//PB14
#define RF_Pin_All RF_fl_Pin|RF_sl_Pin|RF_fr_Pin|RF_sr_Pin	//ȫ����������

extern int rf_fl,rf_sl,rf_fr,rf_sr; 	//�ⲿ����

void RF_Init(void);		//�����ʼ��
void rf_read(void);		//��ȡ����״̬

#endif
