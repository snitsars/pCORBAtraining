#include "..\server_cpp\IHelloWorld.hh"
#include "..\server_cpp\CorbaUtils.h"
#include "TestCallBackImpl.h"
#include <string>
#include <iostream>
#include <sstream>

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

wchar_t* charToWChar(const char* text)
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

#define SYSTEM_EXCEPTION_TYPE 1
#define TRANSIENT_EXCEPTION_TYPE 2

long expectedExceptionType = 0;
bool exceptionProperlyHandled = false;

CORBA::Boolean systemExceptionHandler(void* cookie,
	CORBA::ULong n_retries,
	const CORBA::SystemException& ex)
{
	if (expectedExceptionType == SYSTEM_EXCEPTION_TYPE)
		exceptionProperlyHandled = true;

	return false;
}
CORBA::Boolean transientExceptionHandler(void* cookie,
	CORBA::ULong retries,
	const CORBA::TRANSIENT& ex)
{
	if (expectedExceptionType == TRANSIENT_EXCEPTION_TYPE)
		exceptionProperlyHandled = true;

	return false;  
}

int runTests(CORBA::ORB_var orb, First::IHello_ptr hello)
{
	result = 0;

	try
	{
		std::cout << "  AddValue: ";
		check(5 == hello->AddValue(2, 3));
	}
	catch (...)
	{
		check(false);
	}

	try
	{
		std::cout << "  SayHello: ";
		check(std::wstring(L"Hello, Andy. It's Bob.") == (wchar_t*)CORBA::WString_var(hello->SayHello(L"Andy")));
	}
	catch (...)
	{
		check(false);
	}

	try
	{
		std::cout << "  SayHello2: ";
		CORBA::String_var greeting;
		hello->SayHello2("Andy", greeting.out());
		check(std::string("Hello, Andy. It's Bob.") == (char*)greeting);
	}
	catch (...)
	{
		check(false);
	}

	try
	{
		std::cout << "  Message: ";
		CORBA::String_var message = "Hello, Bob";
		hello->Message(message.inout());
		check(std::string("Hello, Andy.") == (char*)message);
	}
	catch (...)
	{
		check(false);
	}

	try
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
	catch (...)
	{
		check(false);
	}

	try
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
	catch (...)
	{
		check(false);
	}

	try
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
	catch (...)
	{
		check(false);
	}

	try
	{
		std::cout << "  Install exceptions hadlers: ";
		omniORB::installTransientExceptionHandler(hello, 0, transientExceptionHandler);
		omniORB::installSystemExceptionHandler(hello, 0, systemExceptionHandler);
		check(true);
	}
	catch (...)
	{
		check(false);
	}

	try
	{
		std::cout << "  Catch NO_IMPLEMENT: ";
		expectedExceptionType = SYSTEM_EXCEPTION_TYPE;
		exceptionProperlyHandled = false;
		hello->ThrowExceptions(0);
	}
	catch (CORBA::NO_IMPLEMENT& se)
	{
		check(exceptionProperlyHandled && 1 == se.minor());
	}
	catch (...)
	{
		check(false);
	}

	try
	{
		std::cout << "  Catch TRANSIENT: ";
		expectedExceptionType = TRANSIENT_EXCEPTION_TYPE;
		exceptionProperlyHandled = false;
		hello->ThrowExceptions(3);
	}
	catch (CORBA::TRANSIENT& se)
	{
		std::string ex_neame = se._name();
		check(exceptionProperlyHandled && ex_neame.compare("TRANSIENT") == 0);
	}
	catch (...)
	{
		check(false);
	}

	try
	{
		std::cout << "  Catch plain user exception: ";
		hello->ThrowExceptions(1);
	}
	catch (First::IHello::UserExceptionS& ue)
	{
		check(std::string("UserExceptionS") == ue._name());
	}
	catch (...)
	{
		check(false);
	}

	try
	{
		std::cout << "  Catch user exception with members: ";
		hello->ThrowExceptions(2);
	}
	catch (First::IHello::UserExceptionExt& ue)
	{
		check((std::string("EXCEPTIONS_WORKS") == (char*)ue.reason) && (254 == ue.codeError));
	}
	catch (...)
	{
		check(false);
	}

	try
	{
		std::cout << "  Catch unknown exception: ";
		hello->ThrowExceptions(4);
	}
	catch (CORBA::UNKNOWN& se)
	{
		check(std::string("UNKNOWN") == (char*)se._name());
	}
	catch (...)
	{
		check(false);
	}

	try
	{
		std::cout << "  Sequence reversed: ";

		int row[] = { 1, 3, 5, 7, 10 };
		int length = sizeof(row) / sizeof(row[0]);

		First::SequenceLong_var sequence(new First::SequenceLong());
		sequence->length(length);
		for (int i = 0; i < length; ++i)
		{
			sequence[i] = row[i];
		}

		First::SequenceLong_var reversed = hello->Reverse(sequence.in());

		if (5 == reversed->length())
		{
			check((reversed[0] == row[4]) && (reversed[1] == row[3]) && (reversed[2] == row[2]) && (reversed[3] == row[1]) && (reversed[4] == row[0]));
		}
		else
			check(false);
	}
	catch (...)
	{
		check(false);
	}

	try
	{
		std::cout << "  Callback: ";

		PortableServer::POA_var poa = createBidirectionalPOA(orb);

		TestCallBackImpl* pCallback = new TestCallBackImpl();
		PortableServer::ObjectId_var oid = poa->activate_object(pCallback);
		First::ITestCallBack_var callback(pCallback->_this());
		pCallback->_remove_ref();

		check(hello->CallMe(callback) && pCallback->Greeting() == "Hello from Server");
	}
	catch (...)
	{
		check(false);
	}

	try
	{
		std::cout << "  Pass single dimensional array: ";

		First::Vector4_var x = First::Vector4_alloc();
		x[0] = 1.0; x[1] = 2.0; x[2] = 3; x[3] = -4.0;

		First::Vector4_var y = First::Vector4_alloc();
		y[0] = -1.0; y[1] = 12.0; y[2] = 4.1; y[3] = 0;

		double expected[] = {
			x[0] + y[0],
			x[1] + y[1],
			x[2] + y[2],
			x[3] + y[3]
		};

		First::Vector4_slice* result = hello->AddVectors(x, y);
		bool equal = result[0] == expected[0] && result[1] == expected[1] && result[2] == expected[2] && result[3] == expected[3];
		
		First::Vector4_free(result);

		check(equal);
	}
	catch (...)
	{
		check(false);
	}

	try
	{
		std::cout << "  Pass multi dimensional array: ";

		First::Matrix3x4_var x = First::Matrix3x4_alloc();
		x[0][0] =  1.0; x[0][1] = -2.0; x[0][2] =  3; x[0][3] = 4.1;
		x[1][0] =  2.0; x[1][1] =  4.0; x[1][2] = -6; x[1][3] = 8.1;
		x[2][0] = -3.0; x[2][1] = -5.0; x[2][2] =  7; x[2][3] =  -1;

		First::Matrix3x4_var y = First::Matrix3x4_alloc();
		y[0][0] =  3.0; y[0][1] = -2.4; y[0][2] =  3; y[0][3] =  -0;
		y[1][0] =  6.0; y[1][1] =  2.0; y[1][2] = -7; y[1][3] = 8.9;
		y[2][0] = -7.0; y[2][1] = -1.0; y[2][2] =  7; y[2][3] =   1;

		double expected[3][4] = {
			{ x[0][0] + y[0][0], x[0][1] + y[0][1], x[0][2] + y[0][2], x[0][3] + y[0][3] },
			{ x[1][0] + y[1][0], x[1][1] + y[1][1], x[1][2] + y[1][2], x[1][3] + y[1][3] },
			{ x[2][0] + y[2][0], x[2][1] + y[2][1], x[2][2] + y[2][2], x[2][3] + y[2][3] }
		};

		First::Matrix3x4_slice* result = hello->AddMatrixes(x, y);

		//check selectively
		bool equal = result[0][0] == expected[0][0] && result[1][3] == expected[1][3] && result[2][0] == expected[2][0] && result[2][3] == expected[2][3];

		First::Matrix3x4_free(result);

		check(equal);
	}
	catch (...)
	{
		check(false);
	}

	try
	{
		std::cout << "  Shutdown: ";
		hello->Shutdown();
		check(true);
	}
	catch (...)
	{
		check(false);
	}

	return result;
}

int main(int argc, char** argv)
{
	int result = -1;
	CORBA::ORB_var orb = CORBA::ORB_init(argc, argv);
	{
		First::IHello_var service = First::IHello::_narrow(getService(orb, "testService"));

		result = runTests(orb, service);
	
		orb->destroy();
	}

	return result;
}

