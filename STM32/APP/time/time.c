/****************************************************
	功能：定时器中断配置
	资源：TIM4 TIM1 TIM8
	引脚：无
	中断优先级：
		TIM4:
			优先级组别：NVIC_PriorityGroup_1 
			抢占优先级：1 
			副优先级：	1
		TIM1:
			优先级组别：NVIC_PriorityGroup_2 
			抢占优先级：0 
			副优先级：	0
		TIM8:
			优先级组别：NVIC_PriorityGroup_1 
			抢占优先级：1 
			副优先级：	2
	定时频率：
		公式：(72M)/(TIM_Period+1)*(TIM_Prescaler+1)
		具体时间：
			TIM4 (72*10^6)/(19+1)*(35999+1))=100Hz
			TIM1 (72*10^6)/(199+1)*(35999+1))=10Hz
			TIM8 (72*10^6)/(39+1)*(35999+1))=50Hz
****************************************************/

#include "time.h"
void time4_init()		//定时器初始化
{
	NVIC_InitTypeDef NVIC_InitStructure;
	TIM_TimeBaseInitTypeDef TIM_TimeBaseStructure;
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM4,ENABLE);		//定时器时钟使能

	TIM_ClearITPendingBit(TIM4,TIM_IT_Update);
	
	TIM_TimeBaseStructure.TIM_Period = 19;	//定时周期
	TIM_TimeBaseStructure.TIM_Prescaler = 35999;	//预分频
	TIM_TimeBaseStructure.TIM_ClockDivision = 0;	//时钟分频
	TIM_TimeBaseStructure.TIM_CounterMode = TIM_CounterMode_Up;	//向上计数
	TIM_TimeBaseInit(TIM4, & TIM_TimeBaseStructure);
	//TIM_Cmd(TIM4,ENABLE);		//使能或失能相应的TIM外设
	
	TIM_ITConfig(TIM4, TIM_IT_Update, ENABLE );		//使能或失能指定的TIMx
	
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_1);	//中断优先级设置
	NVIC_InitStructure.NVIC_IRQChannel = TIM4_IRQn;
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 1;
	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 1;
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
	NVIC_Init(&NVIC_InitStructure);

}

void time1_init()		//定时器初始化
{
	NVIC_InitTypeDef NVIC_InitStructure;
	TIM_TimeBaseInitTypeDef TIM_TimeBaseStructure;
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_TIM1,ENABLE);		//定时器时钟使能

	
	TIM_TimeBaseStructure.TIM_Period = 199;	//定时周期
	TIM_TimeBaseStructure.TIM_Prescaler = 35999;	//预分频
	TIM_TimeBaseStructure.TIM_ClockDivision = 0;	//时钟分频
	TIM_TimeBaseStructure.TIM_CounterMode = TIM_CounterMode_Up;	//向上计数
	TIM_TimeBaseStructure.TIM_RepetitionCounter = 0;//重复计数设置
	TIM_TimeBaseInit(TIM1, & TIM_TimeBaseStructure);
	//TIM_Cmd(TIM4,ENABLE);		//使能或失能相应的TIM外设
	TIM_ClearFlag(TIM1, TIM_FLAG_Update);//清除中断标志
	TIM_ITConfig(TIM1,TIM_IT_Update|TIM_IT_Trigger,ENABLE);		//使能或失能指定的TIMx

	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);	//中断优先级设置
	NVIC_InitStructure.NVIC_IRQChannel = TIM1_UP_IRQn;
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 0;
	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 0;
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
	NVIC_Init(&NVIC_InitStructure);
	//TIM_Cmd(TIM1, ENABLE);
}

void time8_init()		//定时器初始化
{
	NVIC_InitTypeDef NVIC_InitStructure;
	TIM_TimeBaseInitTypeDef TIM_TimeBaseStructure;
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_TIM8,ENABLE);		//定时器时钟使能

	
	TIM_TimeBaseStructure.TIM_Period = 99;	//定时周期
	TIM_TimeBaseStructure.TIM_Prescaler = 35999;	//预分频
	TIM_TimeBaseStructure.TIM_ClockDivision = 0;	//时钟分频
	TIM_TimeBaseStructure.TIM_CounterMode = TIM_CounterMode_Up;	//向上计数
	TIM_TimeBaseStructure.TIM_RepetitionCounter = 0;//重复计数设置
	TIM_TimeBaseInit(TIM8, & TIM_TimeBaseStructure);
	//TIM_Cmd(TIM8,ENABLE);		//使能或失能相应的TIM外设
	TIM_ClearFlag(TIM8,TIM_FLAG_Update);//清除中断标志
	TIM_ITConfig(TIM8,TIM_IT_Update|TIM_IT_Trigger,ENABLE);		//使能或失能指定的TIMx

	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_1);	//中断优先级设置
	NVIC_InitStructure.NVIC_IRQChannel = TIM8_UP_IRQn;
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 1;
	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 2;
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
	NVIC_Init(&NVIC_InitStructure);
	//TIM_Cmd(TIM8, ENABLE);
}
void time_init()
{
	time4_init();
	time1_init();
	time8_init();
}