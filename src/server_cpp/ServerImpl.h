#pragma once
#include "IHelloWorld.hh"

class CServerImpl : public POA_First::IHello
{
public:
	CServerImpl();
	virtual ~CServerImpl();

	virtual CORBA::Long AddValue(CORBA::Long arg1, CORBA::Long arg2);
	virtual CORBA::WChar* SayHello(const CORBA::WChar* name);
};
