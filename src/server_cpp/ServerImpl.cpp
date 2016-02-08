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

First::MyComplexNumber CServerImpl::MulComplex(const First::MyComplexNumber& x, First::MyComplexNumber& y)
{
	First::MyComplexNumber result;
	result.re = x.re * y.re - x.im * y.im;
	result.im = x.re * y.im + x.im - y.re;

	y = result;

	return result;
}

CORBA::Boolean CServerImpl::MulComplexAsAny(const CORBA::Any& x, const CORBA::Any& y, CORBA::Any_OUT_arg result)
{
	
	First::MyComplexNumber *_x, *_y;
	if(!(x >>= _x))
		return false;

	if(!(y >>= _y))
		return false;

	First::MyComplexNumber _result = MulComplex(*_x, *_y);

	result = new CORBA::Any;
	*result <<= _result;
	
	return true;
}

CORBA::LongLong CServerImpl::GetServerDateTime(CORBA::WString_out serverTime)
{
	char buf[100];
	time_t raw_server_time = time(NULL);
	ctime_s(buf, 100, &raw_server_time);
	serverTime = charToWChar(buf);
	return static_cast<long long>(raw_server_time);
}