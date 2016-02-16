#pragma once

#ifndef __CORBA_H_EXTERNAL_GUARD__
#include <omniORB4/CORBA.h>
#endif

PortableServer::POA_ptr createBidirectionalPOA(CORBA::ORB_var orb)
{
	// Create root POA
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

	return rootpoa->create_POA("bidir", pman, pl);
}

CORBA::Object_ptr getService(CORBA::ORB_ptr orb, const char* serviceName)
{
	CORBA::Object_var objNS = orb->resolve_initial_references("NameService");

	CosNaming::NamingContext_var ns;
	ns = CosNaming::NamingContext::_narrow(objNS);

	CosNaming::Name name;
	name.length(1);
	name[0].id = CORBA::string_dup("testService");

	return ns->resolve(name);
}

void publishService(CORBA::ORB_ptr orb, const CORBA::Object_ptr service, const char* serviceName)
{
	// Obtain a reference to the Name service:
	CORBA::Object_var objNS = orb->resolve_initial_references("NameService");
	CosNaming::NamingContext_var ns = CosNaming::NamingContext::_narrow(objNS);

	CosNaming::Name name;
	name.length(1);
	name[0].id = CORBA::string_dup(serviceName);

	ns->rebind(name, service);
}