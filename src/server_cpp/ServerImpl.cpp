#include "ServerImpl.h"
#include <string>
#include <time.h>
#include <iostream>

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
CORBA::LongLong CServerImpl::GetServerDateTime(CORBA::WString_out serverTime)
{
	char buf[100];
	tm server_time_tm ={0,0,15,5,1,2016,0,1,1};
	time_t server_time_raw = mktime(&server_time_tm);
	ctime_s(buf, 100, &server_time_raw);	
	serverTime = (const CORBA::WChar*)buf;
	

	return static_cast<long int>(server_time_raw);
}