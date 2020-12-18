/****************************************************
	功能：printf配置
	资源：UART1
		波特率：115200
		数据位：8
		停止位：1
		终止位：0
	引脚：tx A9;rx A10
	中断优先级：
		优先级组别：NVIC_PriorityGroup_0 
		抢占优先级：0 
		副优先级：	0
	
****************************************************/
#include "printf.h"

int fputc(int ch,FILE *p)
{
		USART_SendData(USART1, (uint8_t)ch);
		while(USART_GetFlagStatus(USART1, USART_FLAG_TXE)==Bit_RESET);
		return ch;
}

void printf_init()
{
		GPIO_InitTypeDef GPIO_InitStructure;
		USART_InitTypeDef USART_InitStructure;
		NVIC_InitTypeDef NVIC_InitStructure;

	
		RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA,ENABLE);	
		RCC_APB2PeriphClockCmd(RCC_APB2Periph_AFIO,ENABLE);		//复用
		RCC_APB2PeriphClockCmd(RCC_APB2Periph_USART1,ENABLE);		//串口时钟使能

	
		GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
		GPIO_InitStructure.GPIO_Pin = GPIO_Pin_9;				//tx
		GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;		//注意修改
		GPIO_Init(GPIOA,&GPIO_InitStructure);
	

		GPIO_InitStructure.GPIO_Pin = GPIO_Pin_10;			//rx
		GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IN_FLOATING;		//浮空输入
		GPIO_Init(GPIOA,&GPIO_InitStructure);
	
		USART_InitStructure.USART_BaudRate = 115200;
		USART_InitStructure.USART_WordLength = USART_WordLength_8b;
		USART_InitStructure.USART_StopBits = USART_StopBits_1;
		USART_InitStructure.USART_Parity = USART_Parity_No;
		USART_InitStructure.USART_HardwareFlowControl = USART_HardwareFlowControl_None;
		USART_InitStructure.USART_Mode = USART_Mode_Tx | USART_Mode_Rx;
		USART_Init(USART1, &USART_InitStructure);
		
		USART_Cmd(USART1, ENABLE);//使能外设		
		USART_ITConfig(USART1, USART_IT_RXNE,ENABLE);
		USART_ClearFlag(USART1,USART_FLAG_TC);
		
		NVIC_PriorityGroupConfig(NVIC_PriorityGroup_0);
		NVIC_InitStructure.NVIC_IRQChannel = USART1_IRQn;
		NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 0;
		NVIC_InitStructure.NVIC_IRQChannelSubPriority = 0;
		NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
		NVIC_Init(&NVIC_InitStructure);

}
