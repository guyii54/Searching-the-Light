/****************************************************
	功能：PWM配置
	资源：TIM3 
	引脚：B5
	中断优先级：0 2
	定时频率：
		公式：(72M)/(TIM_Period+1)*(TIM_Prescaler+1)
		具体时间：(72*10^6)/(49+1)*(35999+1))=40
****************************************************/

#include "pwm.h"
void pwm_init()//PWM初始化
{
		GPIO_InitTypeDef GPIO_InitStructure;
		TIM_TimeBaseInitTypeDef TIM_TimeBaseStructure;
		TIM_OCInitTypeDef TIM_OCInitStructure;
	
		RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM3,ENABLE);		//TIM3时钟使能
		RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB,ENABLE);	
		RCC_APB2PeriphClockCmd(RCC_APB2Periph_AFIO,ENABLE);		//复用时钟使能
	
		TIM_ClearITPendingBit(TIM3,TIM_IT_Update);	//清除TIM3中断标志位
		
		TIM_TimeBaseStructure.TIM_Period = 900;
		TIM_TimeBaseStructure.TIM_Prescaler = 0;
		TIM_TimeBaseStructure.TIM_ClockDivision = 0;
		TIM_TimeBaseStructure.TIM_CounterMode = TIM_CounterMode_Up;
		TIM_TimeBaseInit(TIM3, & TIM_TimeBaseStructure);
	
		GPIO_PinRemapConfig(GPIO_PartialRemap_TIM3,ENABLE);//部分重映射
	
		TIM_OCInitStructure.TIM_OCMode=TIM_OCMode_PWM1;
		TIM_OCInitStructure.TIM_OutputState=TIM_OutputState_Enable;
		TIM_OCInitStructure.TIM_OCPolarity=TIM_OCPolarity_High;//置高点亮LED
		TIM_OC2Init(TIM3, & TIM_OCInitStructure);
		
		TIM_OC2PreloadConfig(TIM3, TIM_OCPreload_Enable);	
		
		
		GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
		GPIO_InitStructure.GPIO_Pin = GPIO_Pin_5;
		GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;		//注意修改
		GPIO_Init(GPIOB,&GPIO_InitStructure);

		TIM_Cmd(TIM3,ENABLE);		//使能或失能相应的TIM外设
		
}
