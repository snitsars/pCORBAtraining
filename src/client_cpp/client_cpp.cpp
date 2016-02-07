#include "..\server_cpp\IHelloWorld.hh"
#include <string>
#include <iostream>
#include <ctime>

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

inline wchar_t* charToWChar(const char* text)
{
	size_t newsize = strlen(text) + 1;
	wchar_t * wcstring = new wchar_t[newsize];

	// Convert char* string to a wchar_t* string.
	size_t convertedChars = 0;
	mbstowcs_s(&convertedChars, wcstring, newsize, text, _TRUNCATE);
	return wcstring;
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

	std::cout << "  Get server time: ";
	CORBA::WString_var server_time_string_var = L"";
	
	long long server_time_raw = hello->GetServerDateTime(server_time_string_var);
	time_t server_time_t = (time_t)server_time_raw;
	char buf[100];
	ctime_s(buf, 100, &server_time_t);	
	std::cout << "server_time_str = " << buf;
	std::wstring buff_copy = charToWChar(buf);
	std::wstring buff_copy2 = static_cast<std::wstring>(server_time_string_var);
	check(buff_copy.compare(static_cast<std::wstring>(server_time_string_var)));

	return result;
}

