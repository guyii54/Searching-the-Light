#include "smg.h"
uint8_t smgduan[]={0x3F,0x06,0x5B,0x4F,0x66,0x6D,0x7D,0x07,0x7F,0x6F,0x77,0x7C,0x39,0x5E,0x79,0x71};
void smg_init()
{
	GPIO_InitTypeDef GPIO_InitStructure;
	
	SystemInit();
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB,ENABLE);
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_InitStructure.GPIO_Pin=smg_duan;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
	GPIO_Init(GPIOB,&GPIO_InitStructure);
	
}

void static_smg_display()
{
	uint8_t i;
	for (i=0;i<16;i++)
	{
		GPIO_Write(GPIOB,((u16)~(smgduan[i]))<<8);
		delay_ms(1000);
	}
}
