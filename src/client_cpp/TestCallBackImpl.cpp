#include "TestCallBackImpl.h"
#include <iostream>

TestCallBackImpl::TestCallBackImpl()
{
}

TestCallBackImpl::~TestCallBackImpl()
{
}

CORBA::Long TestCallBackImpl::call(::CORBA::Long inputValue)
{
	greeting += "Hello from Server";
	return inputValue+7;
}