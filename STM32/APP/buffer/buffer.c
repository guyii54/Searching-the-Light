/****************************************************
	���ܣ�������
	��Դ������
	���ţ���
	�ж����ȼ�����
	������
		
****************************************************/

#include "buffer.h"

int32_t buffer[5]={0};

void write_buffer(int *buffer_name,int32_t data)
{
	buffer_name[4]=buffer_name[3];
	buffer_name[3]=buffer_name[2];
	buffer_name[2]=buffer_name[1];
	buffer_name[1]=buffer_name[0];
	buffer_name[0]=data;
}


