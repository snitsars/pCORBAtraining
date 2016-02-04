#include "ServerImpl.h"
#include <string>

CServerImpl::CServerImpl()
{
}

CServerImpl::~CServerImpl()
{
}

CORBA::Long CServerImpl::AddValue(CORBA::Long arg1, CORBA::Long arg2)
{
	return arg1 + arg2;
}

CORBA::WChar* CServerImpl::SayHello(const CORBA::WChar* name)
{
	std::wstring result = L"Hello by CORBA, " + std::wstring(name) + L".";
	return CORBA::wstring_dup(result.c_str());
}