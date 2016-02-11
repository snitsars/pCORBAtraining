#include "TestCallBackImpl.h"

TestCallBackImpl::TestCallBackImpl()
{
}

TestCallBackImpl::~TestCallBackImpl()
{
	std::cout << "~TestCallBackImpl() \n";
}

CORBA::Long TestCallBackImpl::getValue(::CORBA::Long inputValue)
{
	return inputValue;
}