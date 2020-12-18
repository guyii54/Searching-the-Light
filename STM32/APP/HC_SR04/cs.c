/************************************
	功能：超声波模块配置
	资源：TIM2
	引脚：trig PB14;echo PB15
	中断优先级：
		优先级组别：NVIC_PriorityGroup_1
		抢占优先级：0
		副优先级：	2
**************************************/
#include "cs.h"
#include "stm32f10x.h"
#include "SysTick.h"
#include "printf.h"

/*记录定时器溢出次数*/
uint overcount=0;

/*设置中断优先级*/
void NVIC_Config(void)
{
	NVIC_InitTypeDef NVIC_InitStructer;

	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_1);

	NVIC_InitStructer.NVIC_IRQChannelPreemptionPriority=0;
	NVIC_InitStructer.NVIC_IRQChannelSubPriority=2;
	NVIC_InitStructer.NVIC_IRQChannel=TIM2_IRQn;
	NVIC_InitStructer.NVIC_IRQChannelCmd=ENABLE;

	NVIC_Init(&NVIC_InitStructer);
}

/*初始化模块的GPIO以及初始化定时器TIM2*/
void ch_sr04_init(void)
{
	GPIO_InitTypeDef GPIO_InitStructer;
	TIM_TimeBaseInitTypeDef TIM_TimeBaseInitStructer;

	RCC_APB2PeriphClockCmd( RCC_APB2Periph_GPIOB, ENABLE);
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM2, ENABLE);

	/*TRIG触发信号*/
	GPIO_InitStructer.GPIO_Speed=GPIO_Speed_50MHz;
	GPIO_InitStructer.GPIO_Mode=GPIO_Mode_Out_PP;
	GPIO_InitStructer.GPIO_Pin=pin_cs_trig;
	GPIO_Init(GPIOB, &GPIO_InitStructer);

	/*ECOH回响信号*/
	GPIO_InitStructer.GPIO_Mode=GPIO_Mode_IN_FLOATING;
	GPIO_InitStructer.GPIO_Pin=pin_cs_echo;
	GPIO_Init(GPIOB, & GPIO_InitStructer);

	/*定时器TIM2初始化*/
	TIM_DeInit(TIM2);
	TIM_TimeBaseInitStructer.TIM_Period=999;//定时周期为1000
	TIM_TimeBaseInitStructer.TIM_Prescaler=71; //分频系数72
	TIM_TimeBaseInitStructer.TIM_ClockDivision=TIM_CKD_DIV1;//不分频
	TIM_TimeBaseInitStructer.TIM_CounterMode=TIM_CounterMode_Up;
	TIM_TimeBaseInit(TIM2,&TIM_TimeBaseInitStructer);

	TIM_ITConfig(TIM2,TIM_IT_Update,ENABLE);//开启更新中断
	NVIC_Config();
	TIM_Cmd(TIM2,DISABLE);//关闭定时器使能

}



float Senor_Using(void)
{
	float length=0;
	u16 tim;
	int data_true_flag = 1;
	uint32_t lost_count = 0;
	GPIO_SetBits(GPIOB,pin_cs_trig); //拉高信号，作为触发信号
	delay_us(20); //高电平信号超过10us
	GPIO_ResetBits(GPIOB,pin_cs_trig);
	/*等待回响信号*/
	while(GPIO_ReadInputDataBit(GPIOB,pin_cs_echo)==RESET);

	TIM_Cmd(TIM2,ENABLE);//回响信号到来，开启定时器计数

	while(GPIO_ReadInputDataBit(GPIOB,pin_cs_echo)==SET)//回响信号消失
	{
		lost_count++;
		if (lost_count>7000)
		{
			data_true_flag = 0;
			break;			
		}
	}
	TIM_Cmd(TIM2,DISABLE);//关闭定时器
	if (data_true_flag ==1)
	{
		tim=TIM_GetCounter(TIM2);//获取计TIM2数寄存器中的计数值，一边计算回响信号时间
		length=(tim+overcount*1000)/58.0;//通过回响信号计算距离
	}
	else
	{
		length=0;
	}
	TIM2->CNT=0; //将TIM2计数寄存器的计数值清零
	overcount=0; //中断溢出次数清零
	//delay_ms(1);
//	if (length>100)
//	{
//		
//		printf("lost_count is %d\r\n",lost_count);
//	}
	return length;//距离作为函数返回值
}



void TIM2_IRQHandler(void) //中断，当回响信号很长是，计数值溢出后重复计数，用中断来保存溢出次数
{
	if(TIM_GetITStatus(TIM2,TIM_IT_Update)!=RESET)
	{
		TIM_ClearITPendingBit(TIM2,TIM_IT_Update);//清除中断标志
		overcount++;
	}
}
