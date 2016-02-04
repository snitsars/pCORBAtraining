#include "..\server_cpp\IHelloWorld.hh"
#include <string>

class ORBHolder
{
	CORBA::ORB_var mORB;
	First::IHello_ptr mpHello;
public:

	ORBHolder(int argc, char** argv)
	{
		mORB = CORBA::ORB_init(argc, argv);

		CORBA::Object_var objNS = mORB->resolve_initial_references("NameService");

		CosNaming::NamingContext_var ns;
		ns = CosNaming::NamingContext::_narrow(objNS);

		CosNaming::Name name;
		name.length(1);
		name[0].id = CORBA::string_dup("testService");

		CORBA::Object_var obj1 = ns->resolve(name);
		mpHello = First::IHello::_narrow(obj1.in());
	}

	~ORBHolder()
	{
		mORB->destroy();
	}

	First::IHello_ptr getHello() const
	{
		return mpHello;
	}
};

int main(int argc, char** argv)
{
	ORBHolder holder(argc, argv);
	First::IHello_ptr hello = holder.getHello();

	if (5 != hello->AddValue(2, 3))
		return -1;

	//if (std::wstring(L"Hello by CORBA, Andy.") != (wchar_t*)CORBA::WString_var(hello->SayHello(L"Andy")))
	//	return -1;

    return 0;
}

