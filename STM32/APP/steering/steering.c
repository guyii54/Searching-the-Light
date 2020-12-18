/****************************************************
	功能：舵机配置
	资源：TIM3
	引脚：PB5
	中断优先级：无
	PWM输出频率：
		公式：(72M)/(TIM_Period+1)*(TIM_Prescaler+1)
		具体频率：(72*10^6)/(9999+1)*(71+1))=100Hz
		单个计数时间：1us
		周期：10ms
	舵机有效作用区间：0.5ms~2.5ms
****************************************************/

#include "steering.h"
#include "SysTick.h"
#include "beep.h"
#define steering_time 750

void steering_init()//舵机初始化
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
	
		GPIO_PinRemapConfig(GPIO_PartialRemap_TIM3,ENABLE);//部分重映射
	
		TIM_OCInitStructure.TIM_OCMode=TIM_OCMode_PWM1;
		TIM_OCInitStructure.TIM_OutputState=TIM_OutputState_Enable;
		TIM_OCInitStructure.TIM_OCPolarity=TIM_OCPolarity_High;
		TIM_OC2Init(TIM3, & TIM_OCInitStructure);
		
		TIM_OC2PreloadConfig(TIM3, TIM_OCPreload_Enable);	
		
		GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
		GPIO_InitStructure.GPIO_Pin = steering_pin;
		GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;		//注意修改
		GPIO_Init(GPIOB,&GPIO_InitStructure);

		TIM_Cmd(TIM3,ENABLE);		//使能
}

void steering_chg(uint16_t angle)	//给定脉宽
{
	TIM_SetCompare2(TIM3,angle);
}

void steering_out(void)		//伸出舵机
{
	TIM_SetCompare2(TIM3,1500);	//1.5ms
	delay_ms(steering_time);
}

void steering_in(void)		//收回舵机
{
	TIM_SetCompare2(TIM3,500);		//0.5ms
	delay_ms(steering_time);
}

void steering_out_in(void)	//舵机伸出收回函数
{
	GPIO_ResetBits(GPIOB,BEEP_Pin);
	steering_out();
	//delay_ms(1000);
	GPIO_SetBits(GPIOB,BEEP_Pin);	
	steering_in();
	//delay_ms(1000);
	
}