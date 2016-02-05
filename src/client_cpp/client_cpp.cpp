#include "..\server_cpp\IHelloWorld.hh"
#include <string>
#include <iostream>

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

int result;

void check(bool status)
{
	if (!status)
	{
		std::cout << "FALSE\n";
		result = -1;
	}
	else
		std::cout << "OK\n";
}

int main(int argc, char** argv)
{
	ORBHolder holder(argc, argv);
	First::IHello_ptr hello = holder.getHello();

	result = 0;

	std::cout << "  AddValue: ";
	check(5 == hello->AddValue(2, 3));

	std::cout << "  SayHello: ";
	check(std::wstring(L"Hello, Andy. It's Bob.") == (wchar_t*)CORBA::WString_var(hello->SayHello(L"Andy")));

	std::cout << "  SayHello2: ";
	CORBA::String_var greeting;
	hello->SayHello2("Andy", greeting.out());
	check(std::string("Hello, Andy. It's Bob.") == (char*)greeting);
	
	std::cout << "  Message: ";
	CORBA::String_var message = "Hello, Bob";
	hello->Message(message.inout());
	check(std::string("Hello, Andy. It's Bob.") == (char*)greeting);

	return result;
}

