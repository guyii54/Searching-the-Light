#ifndef _RF_H
#define _RF_H
#include "stm32f10x.h"
#define RF_fl_Pin GPIO_Pin_8	//PB8
#define RF_sl_Pin GPIO_Pin_11	//PB11
#define RF_fr_Pin GPIO_Pin_12	//PB12
#define RF_sr_Pin GPIO_Pin_14	//PB14
#define RF_Pin_All RF_fl_Pin|RF_sl_Pin|RF_fr_Pin|RF_sr_Pin	//全部红外引脚

extern int rf_fl,rf_sl,rf_fr,rf_sr; 	//外部变量

void RF_Init(void);		//红外初始化
void rf_read(void);		//读取红外状态

#endif
