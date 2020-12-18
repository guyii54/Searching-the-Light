/***********************
	功能：LED
	资源：无 
	引脚：PA1
	中断优先级：无
************************/

#include "LED.h"
#include "SysTick.h"

void LED_Init()	//LED初始化函数
{
	GPIO_InitTypeDef GPIO_InitStructure;
	
	SystemInit();
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA,ENABLE);
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_InitStructure.GPIO_Pin = LED_Pin;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
	GPIO_Init(GPIOA,&GPIO_InitStructure);
	
}

void LED_Display()	//LED闪烁
{
	GPIO_SetBits(GPIOA, LED_Pin);
	delay_ms(500);
	GPIO_ResetBits(GPIOA, LED_Pin);
	delay_ms(500);
}


void LED_OFF()	//LED关闭
{
	GPIO_SetBits(GPIOA,LED_Pin);
}

void LED_ON()		//LED打开
{
	GPIO_ResetBits(GPIOA,LED_Pin);
}

void LED_Change()	//LED改变状态
{
	if(GPIO_ReadOutputDataBit(GPIOA,LED_Pin)==Bit_SET)
	{
		LED_ON();
	}
	else if(GPIO_ReadOutputDataBit(GPIOA,LED_Pin)==Bit_RESET)
	{
		LED_OFF();
	}
}

void LED_Rxsuccess()	//UART中接收成功闪烁
{
	int i;
	for(i=0;i<3;i++)
	{
		LED_ON();
		delay_ms(500);
		LED_OFF();
		delay_ms(500);
	}
}

void LED_Rxfail()		//UART中接收失败闪烁
{
	LED_ON();
	delay_ms(1000);
	LED_OFF();
	delay_ms(500);
	LED_ON();
	delay_ms(1000);
	LED_OFF();
}


		
