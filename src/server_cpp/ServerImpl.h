#pragma once
#include "server.hh"

class CServerImpl : public POA_test::IServer,
	public PortableServer::RefCountServantBase
{
public:
	CServerImpl();
	virtual ~CServerImpl();

	virtual CORBA::Long add(CORBA::Long arg1, CORBA::Long arg2);
};
