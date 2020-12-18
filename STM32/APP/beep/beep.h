#ifndef _BEEP_H
#define _BEEP_H
#include "stm32f10x.h"
#define BEEP_Pin GPIO_Pin_1

void BEEP_Init(void);			//蜂鸣器初始化函数
void beep_change(void);		//改变蜂鸣器状态
void beep_off(void);			//蜂鸣器关
void beep_on_ms(int time);						//蜂鸣器响，设定时间time(ms)
void beep_on_us(int time);							//蜂鸣器响，设定时间time(us)

#endif
