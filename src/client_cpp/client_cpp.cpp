#include "..\server_cpp\server.hh"
#include <iostream>

int main(int argc, char** argv)
{
	CORBA::ORB_var orb = CORBA::ORB_init(argc, argv);

	CORBA::Object_var objNS = orb->resolve_initial_references("NameService");

	CosNaming::NamingContext_var ns;
	ns = CosNaming::NamingContext::_narrow(objNS);

	CosNaming::Name name;
	name.length(1);
	name[0].id = CORBA::string_dup("testService");

	CORBA::Object_var obj1 = ns->resolve(name);
	test::IServer_ptr ref = test::IServer::_narrow(obj1.in());

	std::cout << "2 + 3 = " << ref->add(2, 3);

	orb->destroy();

    return 0;
}

