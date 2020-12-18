/****************************************************
	���ܣ�printf����
	��Դ��UART1
		�����ʣ�115200
		����λ��8
		ֹͣλ��1
		��ֹλ��0
	���ţ�tx A9;rx A10
	�ж����ȼ���
		���ȼ����NVIC_PriorityGroup_0 
		��ռ���ȼ���0 
		�����ȼ���	0
	
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
		RCC_APB2PeriphClockCmd(RCC_APB2Periph_AFIO,ENABLE);		//����
		RCC_APB2PeriphClockCmd(RCC_APB2Periph_USART1,ENABLE);		//����ʱ��ʹ��

	
		GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
		GPIO_InitStructure.GPIO_Pin = GPIO_Pin_9;				//tx
		GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;		//ע���޸�
		GPIO_Init(GPIOA,&GPIO_InitStructure);
	

		GPIO_InitStructure.GPIO_Pin = GPIO_Pin_10;			//rx
		GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IN_FLOATING;		//��������
		GPIO_Init(GPIOA,&GPIO_InitStructure);
	
		USART_InitStructure.USART_BaudRate = 115200;
		USART_InitStructure.USART_WordLength = USART_WordLength_8b;
		USART_InitStructure.USART_StopBits = USART_StopBits_1;
		USART_InitStructure.USART_Parity = USART_Parity_No;
		USART_InitStructure.USART_HardwareFlowControl = USART_HardwareFlowControl_None;
		USART_InitStructure.USART_Mode = USART_Mode_Tx | USART_Mode_Rx;
		USART_Init(USART1, &USART_InitStructure);
		
		USART_Cmd(USART1, ENABLE);//ʹ������		
		USART_ITConfig(USART1, USART_IT_RXNE,ENABLE);
		USART_ClearFlag(USART1,USART_FLAG_TC);
		
		NVIC_PriorityGroupConfig(NVIC_PriorityGroup_0);
		NVIC_InitStructure.NVIC_IRQChannel = USART1_IRQn;
		NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 0;
		NVIC_InitStructure.NVIC_IRQChannelSubPriority = 0;
		NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
		NVIC_Init(&NVIC_InitStructure);

}
