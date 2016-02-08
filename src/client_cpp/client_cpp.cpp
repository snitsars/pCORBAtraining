#include "..\server_cpp\IHelloWorld.hh"
#include <string>
#include <iostream>
#include <sstream>

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

__int64 FileTimeToInt64(const FILETIME& time_value)
{
	__int64 res = (__int64(time_value.dwHighDateTime) << 32) | __int64(time_value.dwLowDateTime);

	return res;
}

__int64 SysytemTimeToInt64(const SYSTEMTIME& time_value)
{
	FILETIME ft;

	BOOL errorFlag = SystemTimeToFileTime(&time_value, &ft);
	__int64 res = FileTimeToInt64(ft);

	if (errorFlag == 0)
		res = -1;

	return res;
}

void Int64ToFileTime(const __int64 * time_value_p, FILETIME *const ft)
{
	ULARGE_INTEGER li;

	li.QuadPart = *time_value_p;
	ft->dwHighDateTime = li.HighPart;
	ft->dwLowDateTime = li.LowPart;
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

bool equal(const First::MyComplexNumber& x, const First::MyComplexNumber& y)
{
	return x.re == y.re && x.im == y.im;
}

std::string dump(First::MyComplexNumber number)
{
	std::stringstream ss;
	ss << "(" << number.re << ", " << number.im << ")";
	return ss.str();
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
	{
		std::cout << "  SayHello2: ";
		CORBA::String_var greeting;
		hello->SayHello2("Andy", greeting.out());
		check(std::string("Hello, Andy. It's Bob.") == (char*)greeting);
	}
	{
		std::cout << "  Message: ";
		CORBA::String_var message = "Hello, Bob";
		hello->Message(message.inout());
		check(std::string("Hello, Andy.") == (char*)message);
	}
	{
		std::cout << "  MulComplex: ";
		First::MyComplexNumber x, y;
		x.re = 2, x.im = 3;
		y.re = 5, y.im = 6;
		First::MyComplexNumber expected;
		expected.re = x.re * y.re - x.im * y.im;
		expected.im = x.re * y.im + x.im - y.re;

		First::MyComplexNumber result = hello->MulComplex(x, y);
		check(equal(result, expected) && equal(result, y));
	}

	{
		std::cout << "  MulComplexAsAny: ";
		First::MyComplexNumber x, y;
		x.re = 2, x.im = 3;
		y.re = 5, y.im = 6;
		First::MyComplexNumber expected;
		expected.re = x.re * y.re - x.im * y.im;
		expected.im = x.re * y.im + x.im - y.re;

		CORBA::Any _x, _y;
		_x <<= x;
		_y <<= y;

		CORBA::Any_var _result;
		bool success = hello->MulComplexAsAny(_x, _y, _result.out());

		First::MyComplexNumber* result;
		_result >>= result;
		
		check(success && result && equal(*result, expected));
	}
	{
		std::cout << "  DataTimeTransfer: ";
		SYSTEMTIME initial_systemtime = {};
		initial_systemtime.wMilliseconds = 0;
		initial_systemtime.wSecond = 0;
		initial_systemtime.wMinute = 0;
		initial_systemtime.wHour = 0;
		initial_systemtime.wDay = 8;
		initial_systemtime.wDayOfWeek = 1;
		initial_systemtime.wMonth = 2;
		initial_systemtime.wYear = 2016;

		FILETIME initial_filetime;
		SystemTimeToFileTime(&initial_systemtime, &initial_filetime);
		__int64 val = SysytemTimeToInt64(initial_systemtime);

		hello->DataTimeTransfer(val);

		FILETIME return_filetime;
		Int64ToFileTime(&val, &return_filetime);
	
		check(CompareFileTime(&initial_filetime, &return_filetime) == 0);
	}

	return result;
}

