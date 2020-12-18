#include "public.h"

#define BUF_NUM  5		//ÿ���������洢���źŸ���

/*****************�ⲿ��������*******************/
extern u8 ENCODER_BUF[BUF_NUM];	//����������
extern int32_t real_speed_left,real_speed_right;
extern int rf_fl,rf_sl,rf_fr,rf_sr;
extern int32_t buffer[5];
extern float cs_dis;
extern int lost_count;

/****************ȫ�ֱ���**********************/
static int cs_flag=0;
static int beep_flag=0;
uint16_t CS_BUF[BUF_NUM];		//����������,ÿһλΪһ��16λ����
u8 RF_BUF[BUF_NUM];

/*****************��ʼ����������**************/
void init_all()  
{
	printf_init();
	ch_sr04_init();
	steering_init();
	Encoder_Init(0XFFFFFFFF,84-1);
	time_init();
	LED_Init();
	usart_init();
	BEEP_Init();
	exti_init();
	RF_Init();
	//CS_BUF[0] = 24;
	
}

/*****************Ԥ����**********************/
void pre_func()
{
	beep_on_ms(300);
	beep_off();
	delay_ms(500);
	
	steering_in();
	TIM_Cmd(TIM4,ENABLE);
	TIM_Cmd(TIM1, ENABLE);
	//TIM_Cmd(TIM8, ENABLE);
}

/*****************���������Ժ���***************/
void main_test(void)
{
	//steering_test();		//�������
	//beep_on();					//
	//LED_OFF();
	//delay_ms(1000);
	//beep_off();
	//LED_ON();
	//delay_ms(1000);
	//printf("%d  %d  %d  %d\r\n",rf_read(0),rf_read(1),rf_read(2),rf_read(3));
}

int main()
{
	uint32_t d1=1;
	u8 s[] = "st556nd";
	u8 len;		//���ܳ���
	u8 i;
	u8 res;		//���ܼĴ���
	int tmp=0;
	init_all();		//��ʼ����������
	pre_func();		//Ԥ������
	
	while(1)
	{
		main_test();		//���ò���
		//write_buffer(tmp);	//д����
		//tmp++;
		//LED_Change();		//����״ָ̬ʾ
		//printf("cs_flag is %d \r\n",cs_flag);
		
		//beep_off();			//�رշ�����
//		if(cs_flag==1)	//�����Ƿ�����־
//		{
//			//printf("cs is meassuring\r\n");
//			cs_dis=Senor_Using();
//			
//		}
		if((USART_FLAG & 0xC000) == 0xC000)	//USART_FLAGǰ��λ��Ϊ1�����յ����ź�
		{
			
			len = (USART_FLAG & 0x3FFF );
			if(len == 2)
			{
				USART_FLAG = 0;
				printf("%1d%1d%1d%1d %4d %4d",rf_fl,rf_sl,rf_fr,rf_sr,real_speed_left,real_speed_right);	//�����з�16Bytes �������з�14bytes
			}
			if(len == 5)	//ֻ�ж���ݮ�ɷ����źŵĸ�������ݮ��Ӧ����s12345d
			{
				USART_FLAG = 0;
				printf("%5d %4d %4d",(int)(cs_dis*100),real_speed_left,real_speed_right);	//cs_dis*100ת�������� �����з�17Bytes  �������з�15bytes
				//printf("%5d",(int)(cs_dis*100));	//cs_dis*100ת��������
				/*
				if ((int)(cs_dis*100)>=10000)
				{
					printf("lost_count:%d\r\n",lost_count);
				}
				*/
			}
			else if(len == 6)
			{
				USART_FLAG = 0;
				steering_out_in();
			}
			else if(len == 1)
			{
				USART_FLAG = 0;
				TIM_Cmd(TIM8, ENABLE);
				//cs_flag = 1;
				//printf("cs start %d\r\n",cs_flag);
			}
			else if(len == 3)
			{
				USART_FLAG = 0;
				TIM_Cmd(TIM8, DISABLE);
				//cs_flag = 0;
				cs_dis = 0;
				//printf("cs stop  %d\r\n",cs_flag);				
			}
			else
			{
				USART_FLAG = 0;
				//LED_Rxfail();
			}
			beep_on_us(500);
			beep_off();
			
//			for (i=0;i<len;i++)
//				res = USART_RX_BUF[i];
//			USART_FLAG = 0;
//			LED_Rxsuccess();
		}
		    
	}
}

