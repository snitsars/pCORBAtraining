#include "ServerImpl.h"
#include <string>
#include <time.h>
#include <iostream>

CServerImpl::CServerImpl(CORBA::ORB_ptr pORB) : mpORB(pORB)
{
}

CServerImpl::~CServerImpl()
{
}

void CServerImpl::Shutdown()
{
	mpORB->shutdown(0);
}

CORBA::Long CServerImpl::AddValue(CORBA::Long arg1, CORBA::Long arg2)
{
	return arg1 + arg2;
}

CORBA::WChar* CServerImpl::SayHello(const CORBA::WChar* name)
{
	std::wstring result = L"Hello, " + std::wstring(name) + L". It's Bob.";
	return CORBA::wstring_dup(result.c_str());
}

void CServerImpl::SayHello2(const char* name, CORBA::String_out greeting)
{
	std::string result("Hello, " + std::string(name) + ". It's Bob.");
	greeting = result.c_str();
}

CORBA::Boolean CServerImpl::Message(char*& message)
{
	if (strcmp(message, "Hello, Bob") != 0)
		return false;

	CORBA::string_free(message);
	message = CORBA::string_dup("Hello, Andy.");

	return true;
}

First::MyComplexNumber CServerImpl::MulComplex(const First::MyComplexNumber& x, First::MyComplexNumber& y)
{
	First::MyComplexNumber result;
	result.re = x.re * y.re - x.im * y.im;
	result.im = x.re * y.im + x.im - y.re;

	y = result;

	return result;
}

CORBA::Boolean CServerImpl::MulComplexAsAny(const CORBA::Any& x, const CORBA::Any& y, CORBA::Any_OUT_arg result)
{

	First::MyComplexNumber *_x, *_y;
	if (!(x >>= _x))
		return false;

	if (!(y >>= _y))
		return false;

	First::MyComplexNumber _result = MulComplex(*_x, *_y);

	result = new CORBA::Any;
	*result <<= _result;

	return true;
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

void CServerImpl::DataTimeTransfer(CORBA::LongLong& DataTimeValue)
{
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

	FILETIME newFt;
	Int64ToFileTime(&DataTimeValue, &newFt);

	if (CompareFileTime(&initial_filetime, &newFt) == 0)
	{
		DataTimeValue = FileTimeToInt64(newFt);
	}
	else DataTimeValue = -1;

}

void CServerImpl::ThrowExceptions(CORBA::Long excptionVariant)
{
	switch (excptionVariant)
	{
	case 0:
	{
		throw CORBA::NO_IMPLEMENT(1,CORBA::COMPLETED_NO);
		break;
	}

	case 1:
	{
		throw First::IHello::UserExceptionS();
		break;
	}
	case 2:
	{
		throw First::IHello::UserExceptionExt("EXCEPTIONS_WORKS", 254);
		break;
	}
	case 3:
	{
		throw CORBA::TRANSIENT();
		break;
	}
	default:
	{
		throw std::exception();
	}
	}
}

First::SequenceLong* CServerImpl::Reverse(const First::SequenceLong& seq)
{
	First::SequenceLong* reversed = new First::SequenceLong();

	unsigned long length = seq.length();
	reversed->length(length);

	for (unsigned long i = 0; i < length; ++i)
	{
		(*reversed)[i] = seq[length - i - 1];
	}
	return reversed;
}

CORBA::Boolean CServerImpl::CallMe(::First::ITestCallBack_ptr callBack)
{
	if (CORBA::is_nil(callBack))
	{
		return false;
	} else
		return 17 == callBack->call(10);
}

First::Vector4_slice* CServerImpl::AddVectors(const First::Vector4 x, const First::Vector4 y)
{
	First::Vector4_slice* result = First::Vector4_alloc();

	for (int i = 0; i < sizeof(First::Vector4) / sizeof(result[0]); ++i)
		result[i] = x[i] + y[i];

	return result;
}

First::Matrix3x4_slice* CServerImpl::AddMatrixes(const First::Matrix3x4 x, const First::Matrix3x4 y)
{
	First::Matrix3x4_slice* result = First::Matrix3x4_alloc();

	for (int i = 0; i < sizeof(First::Matrix3x4) / sizeof(x[0]); ++i) // 3
		for (int j = 0; j < sizeof(x[0]) / sizeof(x[0][0]); ++j) // 4
			result[i][j] = x[i][j] + y[i][j];

	return result;
}