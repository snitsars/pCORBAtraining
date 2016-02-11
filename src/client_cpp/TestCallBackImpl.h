#pragma once
#include "..\server_cpp\IHelloWorld.hh"
#include <string>
#include <iostream>
#include <sstream>

namespace First
{
	class TestCallBackImpl : public POA_First::ITestCallBack
	{
	public:
		TestCallBackImpl();
		~TestCallBackImpl();
		// IDL operations
	
		virtual CORBA::WChar* getDecoratedString(const CORBA::WChar* a_Input);
	};
}