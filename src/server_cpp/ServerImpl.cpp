#include "ServerImpl.h"

CServerImpl::CServerImpl()
{
}

CServerImpl::~CServerImpl()
{
}

CORBA::Long CServerImpl::add(CORBA::Long arg1, CORBA::Long arg2)
{
	return arg1 + arg2;
}