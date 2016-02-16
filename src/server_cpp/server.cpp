#include <iostream>
#include "ServerImpl.h"
#include "CorbaUtils.h"

int main(int argc, char** argv)
{
	CORBA::ORB_var orb = CORBA::ORB_init(argc, argv);
	{

		PortableServer::POA_var poa = createBidirectionalPOA(orb);

		// Create the server
		CServerImpl* myServer = new CServerImpl(orb.in());
		PortableServer::ObjectId_var server_oid = poa->activate_object(myServer);
		CORBA::Object_var objMyServer = myServer->_this();
		myServer->_remove_ref();

		// Publish server name
		publishService(orb, objMyServer.in(), "testService");

		// Run
		orb->run();
	}

	orb->destroy();

    return 0;
}

