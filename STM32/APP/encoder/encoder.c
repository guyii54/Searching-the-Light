/****************************************************
	功能：编码器配置
	资源：TIM5 CH1 CH4
	引脚：
		left_encoder:  lsb:A0 dir:A2
		right_encoder: lsb:A1 dir:A3
	中断优先级：
		L_encoder:
			优先级分组：	NVIC_PriorityGroup_1
			抢占式优先级：0
			副优先级：		0
		R_encoder:
			优先级分组：	NVIC_PriorityGroup_1
			抢占式优先级：0
			副优先级：		1	
****************************************************/

#include "encoder.h"	
#include "led.h"
#include "printf.h"

void Encoder_Init(u32 arr,u16 psc)				//左右舵机初始化函数
{
	TIM5_CH1_Cap_Init(arr,psc);
	TIM5_CH4_Cap_Init(arr,psc);
}

uint8_t  TIM5CH1_CAPTURE_STA=0;		    				
uint32_t	TIM5CH1_CAPTURE_VAL;

void TIM5_CH1_Cap_Init(u32 arr,u16 psc)		//TIM5CH1初始化
{
	GPIO_InitTypeDef GPIO_InitStructure;
	TIM_TimeBaseInitTypeDef  TIM_TimeBaseStructure;
	NVIC_InitTypeDef NVIC_InitStructure;
	TIM_ICInitTypeDef  TIM5_ICInitStructure;
	
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM5,ENABLE);    
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);	
	
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_0|GPIO_Pin_2;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IN_FLOATING;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOA,&GPIO_InitStructure);
  
	TIM_TimeBaseStructure.TIM_Prescaler=psc;
	TIM_TimeBaseStructure.TIM_CounterMode=TIM_CounterMode_Up;
	TIM_TimeBaseStructure.TIM_Period=arr;
	TIM_TimeBaseStructure.TIM_ClockDivision=TIM_CKD_DIV1; 
	TIM_TimeBaseInit(TIM5,&TIM_TimeBaseStructure);
	
	TIM5_ICInitStructure.TIM_Channel = TIM_Channel_1;
	TIM5_ICInitStructure.TIM_ICPolarity = TIM_ICPolarity_Rising;
	TIM5_ICInitStructure.TIM_ICSelection = TIM_ICSelection_DirectTI;
	TIM5_ICInitStructure.TIM_ICPrescaler = TIM_ICPSC_DIV1; 
	TIM5_ICInitStructure.TIM_ICFilter = 0x00;
	TIM_ICInit(TIM5, &TIM5_ICInitStructure);
		
	TIM_ITConfig(TIM5,TIM_IT_Update|TIM_IT_CC1,ENABLE);		
  TIM_Cmd(TIM5,ENABLE);
	
 	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_1);
	NVIC_InitStructure.NVIC_IRQChannel = TIM5_IRQn;
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority=0;
	NVIC_InitStructure.NVIC_IRQChannelSubPriority =0;		
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;		
	NVIC_Init(&NVIC_InitStructure);	
}

uint8_t  TIM5CH4_CAPTURE_STA=0;		    				
uint32_t	TIM5CH4_CAPTURE_VAL;

void TIM5_CH4_Cap_Init(u32 arr,u16 psc)		//TIM5CH4初始化
{
	GPIO_InitTypeDef GPIO_InitStructure;
	TIM_TimeBaseInitTypeDef  TIM_TimeBaseStructure;
	NVIC_InitTypeDef NVIC_InitStructure;
	TIM_ICInitTypeDef  TIM5_ICInitStructure;
	
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM5,ENABLE);    
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);	
	
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_3|GPIO_Pin_5;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IN_FLOATING;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOA,&GPIO_InitStructure);

	TIM_TimeBaseStructure.TIM_Prescaler=psc;
	TIM_TimeBaseStructure.TIM_CounterMode=TIM_CounterMode_Up;
	TIM_TimeBaseStructure.TIM_Period=arr;
	TIM_TimeBaseStructure.TIM_ClockDivision=TIM_CKD_DIV1; 
	TIM_TimeBaseInit(TIM5,&TIM_TimeBaseStructure);
	
	TIM5_ICInitStructure.TIM_Channel = TIM_Channel_4;
	TIM5_ICInitStructure.TIM_ICPolarity = TIM_ICPolarity_Rising;
	TIM5_ICInitStructure.TIM_ICSelection = TIM_ICSelection_DirectTI;
	TIM5_ICInitStructure.TIM_ICPrescaler = TIM_ICPSC_DIV1; 
	TIM5_ICInitStructure.TIM_ICFilter = 0x00;
	TIM_ICInit(TIM5, &TIM5_ICInitStructure);
		
	TIM_ITConfig(TIM5,TIM_IT_Update|TIM_IT_CC4,ENABLE);		
  TIM_Cmd(TIM5,ENABLE);
	
 	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_1);
	NVIC_InitStructure.NVIC_IRQChannel = TIM5_IRQn;
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority=0;
	NVIC_InitStructure.NVIC_IRQChannelSubPriority =1;		
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;		
	NVIC_Init(&NVIC_InitStructure);	
}

//可经由外部调用
int32_t speed_left_count=0;		
int32_t speed_right_count=0;
u8 ENCODER_BUF[ENCODER_BUF_NUM];	//编码器缓存

void TIM5_IRQHandler(void)				//TIM5中断服务函数
{
	uint8_t encoder_dir_left,encoder_dir_right;
	encoder_dir_left =GPIO_ReadInputDataBit(GPIOA,GPIO_Pin_2);		//读取编码器方向位
	encoder_dir_right =GPIO_ReadInputDataBit(GPIOA,GPIO_Pin_5);
	//printf("encoder_dir=%d\r\n",encoder_dir);
	if(TIM_GetITStatus(TIM5, TIM_IT_CC1) != RESET)								//通道1 左编码器
	{
		if(encoder_dir_left==1)
		{
			speed_left_count++;
		}
		else if(encoder_dir_left==0)
		{
			speed_left_count--;
		}
	}
	
	if(TIM_GetITStatus(TIM5, TIM_IT_CC4) != RESET)								//通道4 右编码器
	{
		if(encoder_dir_right==0)
		{
			speed_right_count++;
		}
		else if(encoder_dir_right==1)
		{
			speed_right_count--;
		}
	}
	TIM_ClearITPendingBit(TIM5, TIM_IT_CC1|TIM_IT_CC4|TIM_IT_Update); //清除中断标志位
}




