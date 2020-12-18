/****************************************************
	功能：串口配置
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

#include "usart.h"

u8 USART_RX_BUF[USART_REC_LEN];     //接收缓冲,最大USART_REC_LEN个字节.
//接收状态
//bit15，	接收完成标志
//bit14，	接收到0x0d
//bit13~0，	接收到的有效字节数目
u16 USART_FLAG=0;       //接收状态标记

void usart_init()//串口初始化
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


void USART1_IRQHandler(void)		//USART1中断服务函数
{
//		static uint16_t k;
//		USART_ClearFlag(USART1,USART_FLAG_TC);
//		if(USART_GetITStatus(USART1, USART_IT_RXNE)!=Bit_RESET)
//		{
//			k = USART_ReceiveData(USART1);
//			USART_SendData(USART1, k);
//			while(USART_GetFlagStatus(USART1, USART_FLAG_TXE)==Bit_RESET);
//		}
	u8 res;													
		//当串口接收到数据  RXNE将被置1 ,进入中断
//	if(USART_GetITStatus(USART1, USART_IT_RXNE) != RESET)  //接收中断(接收到的数据必须是0x0d 0x0a结尾)
//		{
//		Res =USART_ReceiveData(USART1);//(USART1->DR);	//读取接收到的数据
//		
//		if((USART_RX_STA&0x8000)==0)//第一位不为1，接收未完成
//			{
//				//第二位为1，接收到了'n'
//			if(USART_RX_STA&0x4000)
//				{
//					//前一次接收到了'n'，但这次不是'd'
//				if(Res!='d')
//					USART_RX_STA=0;//接收错误,重新开始
//				else 
//				{
//					USART_RX_STA|=0x8000;	//接收完成了
//					printf(USART_RX_BUF);
//					LED_Rxsuccess();
//					USART_RX_STA =0;
//					
//				}
//				}
//				
//				//第二位不为1，还在传输信息中，还没收到'n'
//			else 
//				{	
//				if(Res=='n')
//					USART_RX_STA|=0x4000;					 //接收到回车的前一字节  置位状态寄存器
//				else
//					{
//					USART_RX_BUF[USART_RX_STA&0X3FFF]=Res ;			//将接收的数据 存入数组中
//					USART_RX_STA++;									//长度+1 为下一次做准备
//					if(USART_RX_STA>(USART_REC_LEN-1)) USART_RX_STA=0;//接收超时，接收数据错误,重新开始接收	  
//					}		 
//				}
//			}   		 
//     } 
		if(USART_GetITStatus(USART1, USART_IT_RXNE) != RESET)
		{
			res = USART_ReceiveData(USART1);	
			if((USART_FLAG & 0xC000) != 0xC000)	//前两位不全为1，接收未完成
			{
				if( (USART_FLAG & 0x8000) == 0x8000) //第一位为1，已收到s
				{
					if(res == 'd')
					{
						USART_FLAG |= 0x4000; //接收过程中收到'd'
					}
					else
					{
						USART_RX_BUF[USART_FLAG&0X3FFF]=res ;
						USART_FLAG++;		//接收过程中未接收到'd'，继续往Buff中赋值
						if((USART_FLAG&0x3FFF) > (USART_REC_LEN-1)) USART_FLAG = 0; //接收超时
					}
				}
				else //第一位不为1，未收到s
				{
					if(res == 's') USART_FLAG |= 0x8000;  	//接收到s，第一位置1
				}
			}
		}
}


/*****************  发送一个字符 **********************/
void sendbyte(u8 ch)
{
	/* 发送一个字节数据到USART */
	USART_SendData(USART1,ch);
		
	/* 等待发送数据寄存器为空 */
	while (USART_GetFlagStatus(USART1, USART_FLAG_TXE) == RESET);	
}


/******************发送一个16位整数************************/
void sendint(uint16_t num)
{
	USART_SendData(USART1,num);
	while (USART_GetFlagStatus(USART1, USART_FLAG_TXE) == RESET);	
}
	

/*****************  发送字符串 **********************/
//void sendstring(u8 *str)
//{
//	unsigned int k=0;
//  do 
//  {
//      sendbyte(*(str + k) );
//      k++;
//  } while(*(str + k)!='\0');
//  
//  /* 等待发送完成 */
//  while(USART_GetFlagStatus(USART1,USART_FLAG_TC)==RESET)
//  {}
//}
