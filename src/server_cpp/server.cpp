#include <iostream>
#include "ServerImpl.h"

int main(int argc, char** argv)
{
	CORBA::ORB_var orb = CORBA::ORB_init(argc, argv);

	CORBA::Object_var obj = orb->resolve_initial_references("RootPOA");
	PortableServer::POA_var rootpoa = PortableServer::POA::_narrow(obj.in());
	PortableServer::POAManager_var pman = rootpoa->the_POAManager();
	pman->activate();
	
	// Create a POA with the Bidirectional policy
	CORBA::PolicyList pl;
	pl.length(1);
	CORBA::Any a;
	a <<= BiDirPolicy::BOTH;
	pl[0] = orb->create_policy(BiDirPolicy::BIDIRECTIONAL_POLICY_TYPE, a);

	PortableServer::POA_var poa = rootpoa->create_POA("bidir", pman, pl);

	CServerImpl* myServer = new CServerImpl();
	PortableServer::ObjectId_var server_oid = poa->activate_object(myServer);

	CORBA::Object_var objMyServer = myServer->_this();
	CORBA::String_var sior(orb->object_to_string(objMyServer.in()));
	std::cerr << sior << std::endl;


	CORBA::Object_var objNS = orb->resolve_initial_references("NameService");
	CosNaming::NamingContext_var ns = CosNaming::NamingContext::_narrow(objNS);

	CosNaming::Name name;
	name.length(1);
	name[0].id = CORBA::string_dup("testService");
	ns->rebind(name, objMyServer.in());
	
	myServer->_remove_ref();

	/*
	PortableServer::POAManager_var pman = poa->the_POAManager();
	pman->activate();
	*/
	orb->run();
	orb->destroy();

	free(name[0].id);

    return 0;
}

