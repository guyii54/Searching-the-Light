/****************************************************
	���ܣ���������
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

#include "usart.h"

u8 USART_RX_BUF[USART_REC_LEN];     //���ջ���,���USART_REC_LEN���ֽ�.
//����״̬
//bit15��	������ɱ�־
//bit14��	���յ�0x0d
//bit13~0��	���յ�����Ч�ֽ���Ŀ
u16 USART_FLAG=0;       //����״̬���

void usart_init()//���ڳ�ʼ��
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


void USART1_IRQHandler(void)		//USART1�жϷ�����
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
		//�����ڽ��յ�����  RXNE������1 ,�����ж�
//	if(USART_GetITStatus(USART1, USART_IT_RXNE) != RESET)  //�����ж�(���յ������ݱ�����0x0d 0x0a��β)
//		{
//		Res =USART_ReceiveData(USART1);//(USART1->DR);	//��ȡ���յ�������
//		
//		if((USART_RX_STA&0x8000)==0)//��һλ��Ϊ1������δ���
//			{
//				//�ڶ�λΪ1�����յ���'n'
//			if(USART_RX_STA&0x4000)
//				{
//					//ǰһ�ν��յ���'n'������β���'d'
//				if(Res!='d')
//					USART_RX_STA=0;//���մ���,���¿�ʼ
//				else 
//				{
//					USART_RX_STA|=0x8000;	//���������
//					printf(USART_RX_BUF);
//					LED_Rxsuccess();
//					USART_RX_STA =0;
//					
//				}
//				}
//				
//				//�ڶ�λ��Ϊ1�����ڴ�����Ϣ�У���û�յ�'n'
//			else 
//				{	
//				if(Res=='n')
//					USART_RX_STA|=0x4000;					 //���յ��س���ǰһ�ֽ�  ��λ״̬�Ĵ���
//				else
//					{
//					USART_RX_BUF[USART_RX_STA&0X3FFF]=Res ;			//�����յ����� ����������
//					USART_RX_STA++;									//����+1 Ϊ��һ����׼��
//					if(USART_RX_STA>(USART_REC_LEN-1)) USART_RX_STA=0;//���ճ�ʱ���������ݴ���,���¿�ʼ����	  
//					}		 
//				}
//			}   		 
//     } 
		if(USART_GetITStatus(USART1, USART_IT_RXNE) != RESET)
		{
			res = USART_ReceiveData(USART1);	
			if((USART_FLAG & 0xC000) != 0xC000)	//ǰ��λ��ȫΪ1������δ���
			{
				if( (USART_FLAG & 0x8000) == 0x8000) //��һλΪ1�����յ�s
				{
					if(res == 'd')
					{
						USART_FLAG |= 0x4000; //���չ������յ�'d'
					}
					else
					{
						USART_RX_BUF[USART_FLAG&0X3FFF]=res ;
						USART_FLAG++;		//���չ�����δ���յ�'d'��������Buff�и�ֵ
						if((USART_FLAG&0x3FFF) > (USART_REC_LEN-1)) USART_FLAG = 0; //���ճ�ʱ
					}
				}
				else //��һλ��Ϊ1��δ�յ�s
				{
					if(res == 's') USART_FLAG |= 0x8000;  	//���յ�s����һλ��1
				}
			}
		}
}


/*****************  ����һ���ַ� **********************/
void sendbyte(u8 ch)
{
	/* ����һ���ֽ����ݵ�USART */
	USART_SendData(USART1,ch);
		
	/* �ȴ��������ݼĴ���Ϊ�� */
	while (USART_GetFlagStatus(USART1, USART_FLAG_TXE) == RESET);	
}


/******************����һ��16λ����************************/
void sendint(uint16_t num)
{
	USART_SendData(USART1,num);
	while (USART_GetFlagStatus(USART1, USART_FLAG_TXE) == RESET);	
}
	

/*****************  �����ַ��� **********************/
//void sendstring(u8 *str)
//{
//	unsigned int k=0;
//  do 
//  {
//      sendbyte(*(str + k) );
//      k++;
//  } while(*(str + k)!='\0');
//  
//  /* �ȴ�������� */
//  while(USART_GetFlagStatus(USART1,USART_FLAG_TC)==RESET)
//  {}
//}
