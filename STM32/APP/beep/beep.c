/****************************************************
	功能：蜂鸣器配置
	资源：GPIO
	引脚：PB1
	中断优先级：无
	
****************************************************/
#include "beep.h"
#include "SysTick.h"

void BEEP_Init(void)			//蜂鸣器初始化函数
{
	GPIO_InitTypeDef GPIO_InitStructure;
	SystemInit();
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB,ENABLE);
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_InitStructure.GPIO_Pin = BEEP_Pin;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
	GPIO_Init(GPIOB,&GPIO_InitStructure);
	GPIO_SetBits(GPIOB,BEEP_Pin);
}

void beep_change(void)		//改变蜂鸣器状态
{
	if(GPIO_ReadOutputDataBit(GPIOB,BEEP_Pin)==Bit_RESET)
	{
		GPIO_SetBits(GPIOB,BEEP_Pin);		//蜂鸣器不响
	}
	else
	{
		GPIO_ResetBits(GPIOB,BEEP_Pin);	//蜂鸣器响
	}	
}

void beep_off(void)									//蜂鸣器关
{
	GPIO_SetBits(GPIOB,BEEP_Pin);			//蜂鸣器关
}

void beep_on_ms(int time)							//蜂鸣器响，设定时间time(ms)
{
	GPIO_ResetBits(GPIOB,BEEP_Pin);
	delay_ms(time);
}

void beep_on_us(int time)							//蜂鸣器响，设定时间time(us)
{
	GPIO_ResetBits(GPIOB,BEEP_Pin);
	delay_us(time);
}