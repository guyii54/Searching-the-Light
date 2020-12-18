/***********************
	���ܣ�LED
	��Դ���� 
	���ţ�PA1
	�ж����ȼ�����
************************/

#include "LED.h"
#include "SysTick.h"

void LED_Init()	//LED��ʼ������
{
	GPIO_InitTypeDef GPIO_InitStructure;
	
	SystemInit();
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA,ENABLE);
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_InitStructure.GPIO_Pin = LED_Pin;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
	GPIO_Init(GPIOA,&GPIO_InitStructure);
	
}

void LED_Display()	//LED��˸
{
	GPIO_SetBits(GPIOA, LED_Pin);
	delay_ms(500);
	GPIO_ResetBits(GPIOA, LED_Pin);
	delay_ms(500);
}


void LED_OFF()	//LED�ر�
{
	GPIO_SetBits(GPIOA,LED_Pin);
}

void LED_ON()		//LED��
{
	GPIO_ResetBits(GPIOA,LED_Pin);
}

void LED_Change()	//LED�ı�״̬
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

void LED_Rxsuccess()	//UART�н��ճɹ���˸
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

void LED_Rxfail()		//UART�н���ʧ����˸
{
	LED_ON();
	delay_ms(1000);
	LED_OFF();
	delay_ms(500);
	LED_ON();
	delay_ms(1000);
	LED_OFF();
}


		
