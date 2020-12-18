#ifndef __ENCODER_H
#define __ENCODER_H
#include "stm32f10x.h"
#define ENCODER_BUF_NUM 5
extern uint8_t  TIM5CH1_CAPTURE_STA;		    				
extern uint32_t	TIM5CH1_CAPTURE_VAL;

extern uint8_t  TIM5CH4_CAPTURE_STA;		    				
extern uint32_t	TIM5CH4_CAPTURE_VAL;

extern int32_t speed_left_count;		
extern int32_t speed_right_count;
extern u8 ENCODER_BUF[ENCODER_BUF_NUM];			//����������

void TIM5_CH1_Cap_Init(u32 arr,u16 psc);		//TIM5CH1��ʼ��
void TIM5_CH4_Cap_Init(u32 arr,u16 psc);		//TIM5CH4��ʼ��
void Encoder_Init(u32 arr,u16 psc);					//���Ҷ����ʼ������


#endif























