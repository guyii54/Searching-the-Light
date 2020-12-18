#ifndef _usart_H
#define _usart_H
#include "stm32f10x.h"

#define USART_REC_LEN  			10  	//�����������ֽ��� 10
extern u8  USART_RX_BUF[USART_REC_LEN]; //���ջ���,���USART_REC_LEN���ֽ�.ĩ�ֽ�Ϊ���з� 
extern u16 USART_FLAG;         		//����״̬���

void usart_init(void);//���ڳ�ʼ��
void sendbyte(u8 ch);
void sendint(uint16_t num);


#endif
