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
	std::wstring result = L"Hello, " + std::wstring(name) + L". It's Bob.";
	return CORBA::wstring_dup(result.c_str());
}

void CServerImpl::SayHello2(const char* name, CORBA::String_out greeting)
{
	std::string result("Hello, " + std::string(name) + ". It's Bob.");
	greeting = result.c_str();
}

CORBA::Boolean CServerImpl::Message(char*& message)
{
	if (strcmp(message, "Hello, Bob") != 0)
		return false;
	
	CORBA::string_free(message);
	message = CORBA::string_dup("Hello, Andy.");

	return true;
}