#pragma once
#include "..\server_cpp\IHelloWorld.hh"
#include <string>

class TestCallBackImpl : public virtual POA_First::ITestCallBack
{
	std::string greeting;
public:
	TestCallBackImpl();
	virtual ~TestCallBackImpl();
		
	virtual CORBA::Long call(::CORBA::Long inputValue);		
	std::string Greeting() const { return greeting; }
};