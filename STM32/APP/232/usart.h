#ifndef _usart_H
#define _usart_H
#include "stm32f10x.h"

#define USART_REC_LEN  			10  	//定义最大接收字节数 10
extern u8  USART_RX_BUF[USART_REC_LEN]; //接收缓冲,最大USART_REC_LEN个字节.末字节为换行符 
extern u16 USART_FLAG;         		//接收状态标记

void usart_init(void);//串口初始化
void sendbyte(u8 ch);
void sendint(uint16_t num);


#endif
