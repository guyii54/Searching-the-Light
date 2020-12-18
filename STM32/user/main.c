#include "public.h"

#define BUF_NUM  5		//每个传感器存储的信号个数

/*****************外部变量申明*******************/
extern u8 ENCODER_BUF[BUF_NUM];	//编码器缓存
extern int32_t real_speed_left,real_speed_right;
extern int rf_fl,rf_sl,rf_fr,rf_sr;
extern int32_t buffer[5];
extern float cs_dis;
extern int lost_count;

/****************全局变量**********************/
static int cs_flag=0;
static int beep_flag=0;
uint16_t CS_BUF[BUF_NUM];		//超声波缓存,每一位为一个16位整数
u8 RF_BUF[BUF_NUM];

/*****************初始化所有外设**************/
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

/*****************预处理**********************/
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

/*****************主函数测试函数***************/
void main_test(void)
{
	//steering_test();		//舵机测试
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
	u8 len;		//接受长度
	u8 i;
	u8 res;		//接受寄存器
	int tmp=0;
	init_all();		//初始化所有外设
	pre_func();		//预处理部分
	
	while(1)
	{
		main_test();		//调用测试
		//write_buffer(tmp);	//写缓存
		//tmp++;
		//LED_Change();		//运行状态指示
		//printf("cs_flag is %d \r\n",cs_flag);
		
		//beep_off();			//关闭蜂鸣器
//		if(cs_flag==1)	//超声是否开启标志
//		{
//			//printf("cs is meassuring\r\n");
//			cs_dis=Senor_Using();
//			
//		}
		if((USART_FLAG & 0xC000) == 0xC000)	//USART_FLAG前两位均为1，接收到了信号
		{
			
			len = (USART_FLAG & 0x3FFF );
			if(len == 2)
			{
				USART_FLAG = 0;
				printf("%1d%1d%1d%1d %4d %4d",rf_fl,rf_sl,rf_fr,rf_sr,real_speed_left,real_speed_right);	//带换行符16Bytes 不带换行符14bytes
			}
			if(len == 5)	//只判断树莓派发来信号的个数，树莓派应发送s12345d
			{
				USART_FLAG = 0;
				printf("%5d %4d %4d",(int)(cs_dis*100),real_speed_left,real_speed_right);	//cs_dis*100转换成整型 带换行符17Bytes  不带换行符15bytes
				//printf("%5d",(int)(cs_dis*100));	//cs_dis*100转换成整型
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

