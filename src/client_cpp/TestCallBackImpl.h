#pragma once
#include "..\server_cpp\IHelloWorld.hh"
#include <string>
#include <iostream>
#include <sstream>

	class TestCallBackImpl : public POA_First::ITestCallBack
	{
	public:
		TestCallBackImpl();
		~TestCallBackImpl();
		// IDL operations
		CORBA::Long getValue(::CORBA::Long inputValue) override;		
	};