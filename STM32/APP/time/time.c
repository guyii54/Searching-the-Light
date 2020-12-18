/****************************************************
	���ܣ���ʱ���ж�����
	��Դ��TIM4 TIM1 TIM8
	���ţ���
	�ж����ȼ���
		TIM4:
			���ȼ����NVIC_PriorityGroup_1 
			��ռ���ȼ���1 
			�����ȼ���	1
		TIM1:
			���ȼ����NVIC_PriorityGroup_2 
			��ռ���ȼ���0 
			�����ȼ���	0
		TIM8:
			���ȼ����NVIC_PriorityGroup_1 
			��ռ���ȼ���1 
			�����ȼ���	2
	��ʱƵ�ʣ�
		��ʽ��(72M)/(TIM_Period+1)*(TIM_Prescaler+1)
		����ʱ�䣺
			TIM4 (72*10^6)/(19+1)*(35999+1))=100Hz
			TIM1 (72*10^6)/(199+1)*(35999+1))=10Hz
			TIM8 (72*10^6)/(39+1)*(35999+1))=50Hz
****************************************************/

#include "time.h"
void time4_init()		//��ʱ����ʼ��
{
	NVIC_InitTypeDef NVIC_InitStructure;
	TIM_TimeBaseInitTypeDef TIM_TimeBaseStructure;
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM4,ENABLE);		//��ʱ��ʱ��ʹ��

	TIM_ClearITPendingBit(TIM4,TIM_IT_Update);
	
	TIM_TimeBaseStructure.TIM_Period = 19;	//��ʱ����
	TIM_TimeBaseStructure.TIM_Prescaler = 35999;	//Ԥ��Ƶ
	TIM_TimeBaseStructure.TIM_ClockDivision = 0;	//ʱ�ӷ�Ƶ
	TIM_TimeBaseStructure.TIM_CounterMode = TIM_CounterMode_Up;	//���ϼ���
	TIM_TimeBaseInit(TIM4, & TIM_TimeBaseStructure);
	//TIM_Cmd(TIM4,ENABLE);		//ʹ�ܻ�ʧ����Ӧ��TIM����
	
	TIM_ITConfig(TIM4, TIM_IT_Update, ENABLE );		//ʹ�ܻ�ʧ��ָ����TIMx
	
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_1);	//�ж����ȼ�����
	NVIC_InitStructure.NVIC_IRQChannel = TIM4_IRQn;
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 1;
	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 1;
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
	NVIC_Init(&NVIC_InitStructure);

}

void time1_init()		//��ʱ����ʼ��
{
	NVIC_InitTypeDef NVIC_InitStructure;
	TIM_TimeBaseInitTypeDef TIM_TimeBaseStructure;
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_TIM1,ENABLE);		//��ʱ��ʱ��ʹ��

	
	TIM_TimeBaseStructure.TIM_Period = 199;	//��ʱ����
	TIM_TimeBaseStructure.TIM_Prescaler = 35999;	//Ԥ��Ƶ
	TIM_TimeBaseStructure.TIM_ClockDivision = 0;	//ʱ�ӷ�Ƶ
	TIM_TimeBaseStructure.TIM_CounterMode = TIM_CounterMode_Up;	//���ϼ���
	TIM_TimeBaseStructure.TIM_RepetitionCounter = 0;//�ظ���������
	TIM_TimeBaseInit(TIM1, & TIM_TimeBaseStructure);
	//TIM_Cmd(TIM4,ENABLE);		//ʹ�ܻ�ʧ����Ӧ��TIM����
	TIM_ClearFlag(TIM1, TIM_FLAG_Update);//����жϱ�־
	TIM_ITConfig(TIM1,TIM_IT_Update|TIM_IT_Trigger,ENABLE);		//ʹ�ܻ�ʧ��ָ����TIMx

	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);	//�ж����ȼ�����
	NVIC_InitStructure.NVIC_IRQChannel = TIM1_UP_IRQn;
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 0;
	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 0;
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
	NVIC_Init(&NVIC_InitStructure);
	//TIM_Cmd(TIM1, ENABLE);
}

void time8_init()		//��ʱ����ʼ��
{
	NVIC_InitTypeDef NVIC_InitStructure;
	TIM_TimeBaseInitTypeDef TIM_TimeBaseStructure;
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_TIM8,ENABLE);		//��ʱ��ʱ��ʹ��

	
	TIM_TimeBaseStructure.TIM_Period = 99;	//��ʱ����
	TIM_TimeBaseStructure.TIM_Prescaler = 35999;	//Ԥ��Ƶ
	TIM_TimeBaseStructure.TIM_ClockDivision = 0;	//ʱ�ӷ�Ƶ
	TIM_TimeBaseStructure.TIM_CounterMode = TIM_CounterMode_Up;	//���ϼ���
	TIM_TimeBaseStructure.TIM_RepetitionCounter = 0;//�ظ���������
	TIM_TimeBaseInit(TIM8, & TIM_TimeBaseStructure);
	//TIM_Cmd(TIM8,ENABLE);		//ʹ�ܻ�ʧ����Ӧ��TIM����
	TIM_ClearFlag(TIM8,TIM_FLAG_Update);//����жϱ�־
	TIM_ITConfig(TIM8,TIM_IT_Update|TIM_IT_Trigger,ENABLE);		//ʹ�ܻ�ʧ��ָ����TIMx

	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_1);	//�ж����ȼ�����
	NVIC_InitStructure.NVIC_IRQChannel = TIM8_UP_IRQn;
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 1;
	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 2;
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
	NVIC_Init(&NVIC_InitStructure);
	//TIM_Cmd(TIM8, ENABLE);
}
void time_init()
{
	time4_init();
	time1_init();
	time8_init();
}