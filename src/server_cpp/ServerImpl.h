#pragma once
#include "IHelloWorld.hh"
#include <stack>

inline wchar_t* charToWChar(const char* text)
{
	size_t newsize = strlen(text) + 1;
	wchar_t * wcstring = new wchar_t[newsize];

	// Convert char* string to a wchar_t* string.
	size_t convertedChars = 0;
	mbstowcs_s(&convertedChars, wcstring, newsize, text, _TRUNCATE);
	return wcstring;
}


class CServerImpl : public POA_First::IHello
{

public:
	CServerImpl();
	virtual ~CServerImpl();

	virtual CORBA::Long AddValue(CORBA::Long arg1, CORBA::Long arg2);
	virtual CORBA::WChar* SayHello(const CORBA::WChar* name);
	virtual void SayHello2(const char* name, CORBA::String_out greeting);
	virtual CORBA::Boolean Message(char*& message);
	virtual CORBA::LongLong GetServerDateTime(CORBA::WString_out serverTime);

};
