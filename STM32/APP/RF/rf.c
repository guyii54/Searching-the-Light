/****************************************************
	���ܣ���������
	��Դ��GPIO
	���ţ�PB8 PB11 PB12 PB14
	�ж����ȼ�����
	
****************************************************/

#include "rf.h"
void RF_Init(void)	//�����ʼ��
{
	GPIO_InitTypeDef GPIO_InitStructure;
	//SystemInit();
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOC,ENABLE);
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_InitStructure.GPIO_Pin = RF_Pin_All;			//��ʼ���ĸ�����
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;
	GPIO_Init(GPIOC,&GPIO_InitStructure);
}

int rf_fl,rf_sl,rf_fr,rf_sr;	//rf_fl��ǰ��rf_sl������rf_fr��ǰ�ң�rf_sr������
void rf_read(void)		//��ȡ����״̬
{
	rf_fl=GPIO_ReadInputDataBit(GPIOC,RF_fl_Pin);
	rf_sl=GPIO_ReadInputDataBit(GPIOC,RF_sl_Pin);
	rf_fr=GPIO_ReadInputDataBit(GPIOC,RF_fr_Pin);
	rf_sr=GPIO_ReadInputDataBit(GPIOC,RF_sr_Pin);
}
