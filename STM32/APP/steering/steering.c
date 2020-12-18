/****************************************************
	���ܣ��������
	��Դ��TIM3
	���ţ�PB5
	�ж����ȼ�����
	PWM���Ƶ�ʣ�
		��ʽ��(72M)/(TIM_Period+1)*(TIM_Prescaler+1)
		����Ƶ�ʣ�(72*10^6)/(9999+1)*(71+1))=100Hz
		��������ʱ�䣺1us
		���ڣ�10ms
	�����Ч�������䣺0.5ms~2.5ms
****************************************************/

#include "steering.h"
#include "SysTick.h"
#include "beep.h"
#define steering_time 750

void steering_init()//�����ʼ��
{
		GPIO_InitTypeDef GPIO_InitStructure;
		TIM_TimeBaseInitTypeDef TIM_TimeBaseStructure;
		TIM_OCInitTypeDef TIM_OCInitStructure;
	
		RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM3,ENABLE);		
		RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB,ENABLE);	
		RCC_APB2PeriphClockCmd(RCC_APB2Periph_AFIO,ENABLE);	
	
		TIM_ClearITPendingBit(TIM3,TIM_IT_Update);
		
		TIM_TimeBaseStructure.TIM_Period = 9999;
		TIM_TimeBaseStructure.TIM_Prescaler = 71;
		TIM_TimeBaseStructure.TIM_ClockDivision = 0;
		TIM_TimeBaseStructure.TIM_CounterMode = TIM_CounterMode_Up;
		TIM_TimeBaseInit(TIM3, & TIM_TimeBaseStructure);
	
		GPIO_PinRemapConfig(GPIO_PartialRemap_TIM3,ENABLE);//������ӳ��
	
		TIM_OCInitStructure.TIM_OCMode=TIM_OCMode_PWM1;
		TIM_OCInitStructure.TIM_OutputState=TIM_OutputState_Enable;
		TIM_OCInitStructure.TIM_OCPolarity=TIM_OCPolarity_High;
		TIM_OC2Init(TIM3, & TIM_OCInitStructure);
		
		TIM_OC2PreloadConfig(TIM3, TIM_OCPreload_Enable);	
		
		GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
		GPIO_InitStructure.GPIO_Pin = steering_pin;
		GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;		//ע���޸�
		GPIO_Init(GPIOB,&GPIO_InitStructure);

		TIM_Cmd(TIM3,ENABLE);		//ʹ��
}

void steering_chg(uint16_t angle)	//��������
{
	TIM_SetCompare2(TIM3,angle);
}

void steering_out(void)		//������
{
	TIM_SetCompare2(TIM3,1500);	//1.5ms
	delay_ms(steering_time);
}

void steering_in(void)		//�ջض��
{
	TIM_SetCompare2(TIM3,500);		//0.5ms
	delay_ms(steering_time);
}

void steering_out_in(void)	//�������ջغ���
{
	GPIO_ResetBits(GPIOB,BEEP_Pin);
	steering_out();
	//delay_ms(1000);
	GPIO_SetBits(GPIOB,BEEP_Pin);	
	steering_in();
	//delay_ms(1000);
	
}