/****************************************************
	功能：红外配置
	资源：GPIO
	引脚：PB8 PB11 PB12 PB14
	中断优先级：无
	
****************************************************/

#include "rf.h"
void RF_Init(void)	//红外初始化
{
	GPIO_InitTypeDef GPIO_InitStructure;
	//SystemInit();
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOC,ENABLE);
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_InitStructure.GPIO_Pin = RF_Pin_All;			//初始化四个红外
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;
	GPIO_Init(GPIOC,&GPIO_InitStructure);
}

int rf_fl,rf_sl,rf_fr,rf_sr;	//rf_fl：前左；rf_sl：侧左；rf_fr：前右；rf_sr：侧右
void rf_read(void)		//读取红外状态
{
	rf_fl=GPIO_ReadInputDataBit(GPIOC,RF_fl_Pin);
	rf_sl=GPIO_ReadInputDataBit(GPIOC,RF_sl_Pin);
	rf_fr=GPIO_ReadInputDataBit(GPIOC,RF_fr_Pin);
	rf_sr=GPIO_ReadInputDataBit(GPIOC,RF_sr_Pin);
}
