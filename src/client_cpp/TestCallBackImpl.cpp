#include "TestCallBackImpl.h"

First::TestCallBackImpl::TestCallBackImpl()
{
}

First::TestCallBackImpl::~TestCallBackImpl()
{
}

CORBA::WChar* First::TestCallBackImpl::getDecoratedString(const CORBA::WChar* a_Input)
{
	std::wstring result = L"Test done" + (std::wstring)a_Input;
	return &result[0];
}