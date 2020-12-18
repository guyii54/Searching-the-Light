/****************************************************
	���ܣ�����������
	��Դ��GPIO
	���ţ�PB1
	�ж����ȼ�����
	
****************************************************/
#include "beep.h"
#include "SysTick.h"

void BEEP_Init(void)			//��������ʼ������
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

void beep_change(void)		//�ı������״̬
{
	if(GPIO_ReadOutputDataBit(GPIOB,BEEP_Pin)==Bit_RESET)
	{
		GPIO_SetBits(GPIOB,BEEP_Pin);		//����������
	}
	else
	{
		GPIO_ResetBits(GPIOB,BEEP_Pin);	//��������
	}	
}

void beep_off(void)									//��������
{
	GPIO_SetBits(GPIOB,BEEP_Pin);			//��������
}

void beep_on_ms(int time)							//�������죬�趨ʱ��time(ms)
{
	GPIO_ResetBits(GPIOB,BEEP_Pin);
	delay_ms(time);
}

void beep_on_us(int time)							//�������죬�趨ʱ��time(us)
{
	GPIO_ResetBits(GPIOB,BEEP_Pin);
	delay_us(time);
}