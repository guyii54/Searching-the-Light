#ifndef _BUFFER_H
#define _BUFFER_H
#include "stm32f10x.h"

extern int32_t buffer[5];
void write_buffer(int *buffer_name,int32_t data);
	
#endif
