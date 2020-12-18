/**
  ******************************************************************************
  * @file    Project/STM32F10x_StdPeriph_Template/stm32f10x_it.c 
  * @author  MCD Application Team
  * @version V3.5.0
  * @date    08-April-2011
  * @brief   Main Interrupt Service Routines.
  *          This file provides template for all exceptions handler and 
  *          peripherals interrupt service routine.
  ******************************************************************************
  * @attention
  *
  * THE PRESENT FIRMWARE WHICH IS FOR GUIDANCE ONLY AIMS AT PROVIDING CUSTOMERS
  * WITH CODING INFORMATION REGARDING THEIR PRODUCTS IN ORDER FOR THEM TO SAVE
  * TIME. AS A RESULT, STMICROELECTRONICS SHALL NOT BE HELD LIABLE FOR ANY
  * DIRECT, INDIRECT OR CONSEQUENTIAL DAMAGES WITH RESPECT TO ANY CLAIMS ARISING
  * FROM THE CONTENT OF SUCH FIRMWARE AND/OR THE USE MADE BY CUSTOMERS OF THE
  * CODING INFORMATION CONTAINED HEREIN IN CONNECTION WITH THEIR PRODUCTS.
  *
  * <h2><center>&copy; COPYRIGHT 2011 STMicroelectronics</center></h2>
  ******************************************************************************
  */

/* Includes ------------------------------------------------------------------*/
#include "stm32f10x_it.h"
#include "systick.h"
#include "steering.h"
#include "stdlib.h"
#include "printf.h"
#include "rf.h"
#include "cs.h"
#include "beep.h"
#include "LED.h"
/** @addtogroup STM32F10x_StdPeriph_Template
  * @{
  */

/* Private typedef -----------------------------------------------------------*/
/* Private define ------------------------------------------------------------*/
/* Private macro -------------------------------------------------------------*/
/* Private variables ---------------------------------------------------------*/
/* Private function prototypes -----------------------------------------------*/
/* Private functions ---------------------------------------------------------*/

/******************************************************************************/
/*            Cortex-M3 Processor Exceptions Handlers                         */
/******************************************************************************/

/**
  * @brief  This function handles NMI exception.
  * @param  None
  * @retval None
  */
void NMI_Handler(void)
{
}

/**
  * @brief  This function handles Hard Fault exception.
  * @param  None
  * @retval None
  */
void HardFault_Handler(void)
{
  /* Go to infinite loop when Hard Fault exception occurs */
  while (1)
  {
  }
}

/**
  * @brief  This function handles Memory Manage exception.
  * @param  None
  * @retval None
  */
void MemManage_Handler(void)
{
  /* Go to infinite loop when Memory Manage exception occurs */
  while (1)
  {
  }
}

/**
  * @brief  This function handles Bus Fault exception.
  * @param  None
  * @retval None
  */
void BusFault_Handler(void)
{
  /* Go to infinite loop when Bus Fault exception occurs */
  while (1)
  {
  }
}

/**
  * @brief  This function handles Usage Fault exception.
  * @param  None
  * @retval None
  */
void UsageFault_Handler(void)
{
  /* Go to infinite loop when Usage Fault exception occurs */
  while (1)
  {
  }
}

/**
  * @brief  This function handles SVCall exception.
  * @param  None
  * @retval None
  */
void SVC_Handler(void)
{
}

/**
  * @brief  This function handles Debug Monitor exception.
  * @param  None
  * @retval None
  */
/*
void USART1_IRQHandler(void)
{
		static uint16_t k;
		USART_ClearFlag(USART1,USART_FLAG_TC);
		if(USART_GetITStatus(USART1, USART_IT_RXNE)!=Bit_RESET)
		{
			k = USART_ReceiveData(USART1);
			USART_SendData(USART1, k);
			while(USART_GetFlagStatus(USART1, USART_FLAG_TXE)==Bit_RESET);
		}
}
*/

void EXTI0_IRQHandler(void)  //外部中断0处理函数
{
	if(EXTI_GetITStatus(EXTI_Line0)==SET)
	{
		EXTI_ClearITPendingBit(EXTI_Line0);
		delay_ms(500);//消抖处理
		if(GPIO_ReadInputDataBit(GPIOB,GPIO_Pin_0)==Bit_SET)
		{
			delay_ms(10);
			if(GPIO_ReadOutputDataBit(GPIOA,GPIO_Pin_1)==Bit_RESET)
			{
				GPIO_SetBits(GPIOA,GPIO_Pin_1);
			}
			else
			{
				GPIO_ResetBits(GPIOA,GPIO_Pin_1);
			}
		}
		//while(GPIO_ReadInputDataBit(GPIOB,GPIO_Pin_0)==1);
		
	}
	
}

/*void EXTI1_IRQHandler(void)		//外部中断1处理函数
{
	if(EXTI_GetITStatus(EXTI_Line1)==SET)
	{
		EXTI_ClearITPendingBit(EXTI_Line1);
		delay_ms(10);//xiaodou
		if(GPIO_ReadInputDataBit(GPIOA,GPIO_Pin_1)==Bit_RESET)
		{
			delay_ms(10);
			if(GPIO_ReadOutputDataBit(GPIOB,GPIO_Pin_9)==Bit_RESET)
			{
				GPIO_SetBits(GPIOB,GPIO_Pin_9);
			}
			else
			{
				GPIO_ResetBits(GPIOB,GPIO_Pin_9);
			}
		}
		while(GPIO_ReadInputDataBit(GPIOA,GPIO_Pin_1)==0);
		
	}
	
}

void EXTI2_IRQHandler(void)		//外部中断2处理函数
{
	if(EXTI_GetITStatus(EXTI_Line2)==SET)
	{
		EXTI_ClearITPendingBit(EXTI_Line2);
		delay_ms(10);//xiaodou
		if(GPIO_ReadInputDataBit(GPIOA,GPIO_Pin_2)==Bit_RESET)
		{
			delay_ms(10);
			if(GPIO_ReadOutputDataBit(GPIOB,GPIO_Pin_10)==Bit_RESET)
			{
				GPIO_SetBits(GPIOB,GPIO_Pin_10);
			}
			else
			{
				GPIO_ResetBits(GPIOB,GPIO_Pin_10);
			}
		}
		while(GPIO_ReadInputDataBit(GPIOA,GPIO_Pin_2)==0);
		
	}
	
}
*/

void TIM1_UP_IRQHandler(void) 	//TIM1中断服务函数
{ 	    	  	     
	if (TIM_GetITStatus(TIM1, TIM_IT_Update) != RESET)
	{
		TIM_ClearITPendingBit(TIM1, TIM_IT_Update);
		//cs_dis=Senor_Using();
		LED_Change();
		//beep_change();
	}	     
} 



extern int rf_fl,rf_sl,rf_fr,rf_sr;
extern int32_t speed_left_count,speed_right_count;
int32_t real_speed_left,real_speed_right;

void TIM4_IRQHandler(void)
{
	//printf("real_speed_left:%d  real_speed_right:%d\r\n",real_speed_left,real_speed_right);
	//printf("%d  %d  %d  %d\r\n",rf_read(0),rf_read(1),rf_read(2),rf_read(3));
	//printf("%d  %d\r\n",rf_read(0),GPIO_ReadInputDataBit(GPIOC,RF_fl));
	rf_read();
	real_speed_left=speed_left_count;
	real_speed_right=speed_right_count;
	speed_left_count=0;
	speed_right_count=0;
	TIM_ClearITPendingBit(TIM4,TIM_IT_Update);
}


float cs_dis;

void TIM8_UP_IRQHandler(void) 	//TIM8中断服务函数
{ 	    	  	     
	if (TIM_GetITStatus(TIM8, TIM_IT_Update) != RESET)
	{
		TIM_ClearITPendingBit(TIM8, TIM_IT_Update);
		cs_dis=Senor_Using();
		//LED_Change();
	}	     
} 
/*
uint8_t smgduan[]={0x3F,0x06,0x5B,0x4F,0x66,0x6D,0x7D,0x07,0x7F,0x6F,0x77,0x7C,0x39,0x5E,0x79,0x71};

void TIM3_IRQHandler(void)		//定时器流水数码管
{
	static uint8_t	i=0;
	TIM_ClearITPendingBit(TIM3,TIM_IT_Update);
	GPIO_Write(GPIOB,((u16)~(smgduan[i++]))<<8);
	if (i==15)	i=0;

}
*/
void DebugMon_Handler(void)
{
}

/**
  * @brief  This function handles PendSVC exception.
  * @param  None
  * @retval None
  */
void PendSV_Handler(void)
{
}

/**
  * @brief  This function handles SysTick Handler.
  * @param  None
  * @retval None
  */
void SysTick_Handler(void)
{
}

/******************************************************************************/
/*                 STM32F10x Peripherals Interrupt Handlers                   */
/*  Add here the Interrupt Handler for the used peripheral(s) (PPP), for the  */
/*  available peripheral interrupt handler's name please refer to the startup */
/*  file (startup_stm32f10x_xx.s).                                            */
/******************************************************************************/

/**
  * @brief  This function handles PPP interrupt request.
  * @param  None
  * @retval None
  */
/*void PPP_IRQHandler(void)
{
}*/

/**
  * @}
  */ 


/******************* (C) COPYRIGHT 2011 STMicroelectronics *****END OF FILE****/
