#ifndef _smg_H
#define _smg_H
#include "stm32f10x.h"

#define smg_duan GPIO_Pin_8|GPIO_Pin_9|GPIO_Pin_10|GPIO_Pin_11|GPIO_Pin_12|GPIO_Pin_13|GPIO_Pin_14|GPIO_Pin_15

void smg_init(void);
void static_smg_display(void);


#endif
