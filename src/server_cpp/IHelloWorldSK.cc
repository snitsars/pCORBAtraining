// This file is generated by omniidl (C++ backend)- omniORB_4_2. Do not edit.

#include "IHelloWorld.hh"
#include <omniORB4/IOP_S.h>
#include <omniORB4/IOP_C.h>
#include <omniORB4/callDescriptor.h>
#include <omniORB4/callHandle.h>
#include <omniORB4/objTracker.h>


OMNI_USING_NAMESPACE(omni)

static const char* _0RL_library_version = omniORB_4_2;



First::IHello_ptr First::IHello_Helper::_nil() {
  return ::First::IHello::_nil();
}

::CORBA::Boolean First::IHello_Helper::is_nil(::First::IHello_ptr p) {
  return ::CORBA::is_nil(p);

}

void First::IHello_Helper::release(::First::IHello_ptr p) {
  ::CORBA::release(p);
}

void First::IHello_Helper::marshalObjRef(::First::IHello_ptr obj, cdrStream& s) {
  ::First::IHello::_marshalObjRef(obj, s);
}

First::IHello_ptr First::IHello_Helper::unmarshalObjRef(cdrStream& s) {
  return ::First::IHello::_unmarshalObjRef(s);
}

void First::IHello_Helper::duplicate(::First::IHello_ptr obj) {
  if (obj && !obj->_NP_is_nil())  omni::duplicateObjRef(obj);
}

First::IHello_ptr
First::IHello::_duplicate(::First::IHello_ptr obj)
{
  if (obj && !obj->_NP_is_nil())  omni::duplicateObjRef(obj);
  return obj;
}

First::IHello_ptr
First::IHello::_narrow(::CORBA::Object_ptr obj)
{
  if (!obj || obj->_NP_is_nil() || obj->_NP_is_pseudo()) return _nil();
  _ptr_type e = (_ptr_type) obj->_PR_getobj()->_realNarrow(_PD_repoId);
  return e ? e : _nil();
}


First::IHello_ptr
First::IHello::_unchecked_narrow(::CORBA::Object_ptr obj)
{
  if (!obj || obj->_NP_is_nil() || obj->_NP_is_pseudo()) return _nil();
  _ptr_type e = (_ptr_type) obj->_PR_getobj()->_uncheckedNarrow(_PD_repoId);
  return e ? e : _nil();
}

First::IHello_ptr
First::IHello::_nil()
{
#ifdef OMNI_UNLOADABLE_STUBS
  static _objref_IHello _the_nil_obj;
  return &_the_nil_obj;
#else
  static _objref_IHello* _the_nil_ptr = 0;
  if (!_the_nil_ptr) {
    omni::nilRefLock().lock();
    if (!_the_nil_ptr) {
      _the_nil_ptr = new _objref_IHello;
      registerNilCorbaObject(_the_nil_ptr);
    }
    omni::nilRefLock().unlock();
  }
  return _the_nil_ptr;
#endif
}

const char* First::IHello::_PD_repoId = "IDL:Org.Uneta.Iiopnet.Examples/First/IHello:1.0";


First::_objref_IHello::~_objref_IHello() {
  
}


First::_objref_IHello::_objref_IHello(omniIOR* ior, omniIdentity* id) :
   omniObjRef(::First::IHello::_PD_repoId, ior, id, 1)
   
   
{
  _PR_setobj(this);
}

void*
First::_objref_IHello::_ptrToObjRef(const char* id)
{
  if (id == ::First::IHello::_PD_repoId)
    return (::First::IHello_ptr) this;
  
  if (id == ::CORBA::Object::_PD_repoId)
    return (::CORBA::Object_ptr) this;

  if (omni::strMatch(id, ::First::IHello::_PD_repoId))
    return (::First::IHello_ptr) this;
  
  if (omni::strMatch(id, ::CORBA::Object::_PD_repoId))
    return (::CORBA::Object_ptr) this;

  return 0;
}


//
// Code for First::IHello::AddValue

// Proxy call descriptor class. Mangled signature:
//  _clong_i_clong_i_clong
class _0RL_cd_7000e62c77f89b95_00000000
  : public omniCallDescriptor
{
public:
  inline _0RL_cd_7000e62c77f89b95_00000000(LocalCallFn lcfn, const char* op_, size_t oplen, _CORBA_Boolean upcall=0)
    : omniCallDescriptor(lcfn, op_, oplen, 0, _user_exns, 0, upcall)
  {
    
  }
  
  void marshalArguments(cdrStream&);
  void unmarshalArguments(cdrStream&);

  void unmarshalReturnedValues(cdrStream&);
  void marshalReturnedValues(cdrStream&);
  
  
  static const char* const _user_exns[];

  ::CORBA::Long arg_0;
  ::CORBA::Long arg_1;
  ::CORBA::Long result;
};

void _0RL_cd_7000e62c77f89b95_00000000::marshalArguments(cdrStream& _n)
{
  arg_0 >>= _n;
  arg_1 >>= _n;

}

void _0RL_cd_7000e62c77f89b95_00000000::unmarshalArguments(cdrStream& _n)
{
  (::CORBA::Long&)arg_0 <<= _n;
  (::CORBA::Long&)arg_1 <<= _n;

}

void _0RL_cd_7000e62c77f89b95_00000000::marshalReturnedValues(cdrStream& _n)
{
  result >>= _n;

}

void _0RL_cd_7000e62c77f89b95_00000000::unmarshalReturnedValues(cdrStream& _n)
{
  (::CORBA::Long&)result <<= _n;

}

const char* const _0RL_cd_7000e62c77f89b95_00000000::_user_exns[] = {
  0
};

// Local call call-back function.
static void
_0RL_lcfn_7000e62c77f89b95_10000000(omniCallDescriptor* cd, omniServant* svnt)
{
  _0RL_cd_7000e62c77f89b95_00000000* tcd = (_0RL_cd_7000e62c77f89b95_00000000*)cd;
  First::_impl_IHello* impl = (First::_impl_IHello*) svnt->_ptrToInterface(First::IHello::_PD_repoId);
  tcd->result = impl->AddValue(tcd->arg_0, tcd->arg_1);


}

::CORBA::Long First::_objref_IHello::AddValue(::CORBA::Long a, ::CORBA::Long b)
{
  _0RL_cd_7000e62c77f89b95_00000000 _call_desc(_0RL_lcfn_7000e62c77f89b95_10000000, "AddValue", 9);
  _call_desc.arg_0 = a;
  _call_desc.arg_1 = b;

  _invoke(_call_desc);
  return _call_desc.result;


}


//
// Code for First::IHello::SayHello

// Proxy call descriptor class. Mangled signature:
//  _cwstring_i_cwstring
class _0RL_cd_7000e62c77f89b95_20000000
  : public omniCallDescriptor
{
public:
  inline _0RL_cd_7000e62c77f89b95_20000000(LocalCallFn lcfn, const char* op_, size_t oplen, _CORBA_Boolean upcall=0)
    : omniCallDescriptor(lcfn, op_, oplen, 0, _user_exns, 0, upcall)
  {
    
  }
  
  void marshalArguments(cdrStream&);
  void unmarshalArguments(cdrStream&);

  void unmarshalReturnedValues(cdrStream&);
  void marshalReturnedValues(cdrStream&);
  
  
  static const char* const _user_exns[];

  ::CORBA::WString_var arg_0_;
  const ::CORBA::WChar* arg_0;
  ::CORBA::WString_var result;
};

void _0RL_cd_7000e62c77f89b95_20000000::marshalArguments(cdrStream& _n)
{
  _n.marshalWString(arg_0,0);

}

void _0RL_cd_7000e62c77f89b95_20000000::unmarshalArguments(cdrStream& _n)
{
  arg_0_ = _n.unmarshalWString(0);
  arg_0 = arg_0_.in();

}

void _0RL_cd_7000e62c77f89b95_20000000::marshalReturnedValues(cdrStream& _n)
{
  _n.marshalWString(result,0);

}

void _0RL_cd_7000e62c77f89b95_20000000::unmarshalReturnedValues(cdrStream& _n)
{
  result = _n.unmarshalWString(0);

}

const char* const _0RL_cd_7000e62c77f89b95_20000000::_user_exns[] = {
  0
};

// Local call call-back function.
static void
_0RL_lcfn_7000e62c77f89b95_30000000(omniCallDescriptor* cd, omniServant* svnt)
{
  _0RL_cd_7000e62c77f89b95_20000000* tcd = (_0RL_cd_7000e62c77f89b95_20000000*)cd;
  First::_impl_IHello* impl = (First::_impl_IHello*) svnt->_ptrToInterface(First::IHello::_PD_repoId);
  tcd->result = impl->SayHello(tcd->arg_0);


}

::CORBA::WChar* First::_objref_IHello::SayHello(const ::CORBA::WChar* name)
{
  _0RL_cd_7000e62c77f89b95_20000000 _call_desc(_0RL_lcfn_7000e62c77f89b95_30000000, "SayHello", 9);
  _call_desc.arg_0 = name;

  _invoke(_call_desc);
  return _call_desc.result._retn();


}


//
// Code for First::IHello::SayHello2

// Proxy call descriptor class. Mangled signature:
//  void_i_cstring_o_cstring
class _0RL_cd_7000e62c77f89b95_40000000
  : public omniCallDescriptor
{
public:
  inline _0RL_cd_7000e62c77f89b95_40000000(LocalCallFn lcfn, const char* op_, size_t oplen, _CORBA_Boolean upcall=0)
    : omniCallDescriptor(lcfn, op_, oplen, 0, _user_exns, 0, upcall)
  {
    
  }
  
  void marshalArguments(cdrStream&);
  void unmarshalArguments(cdrStream&);

  void unmarshalReturnedValues(cdrStream&);
  void marshalReturnedValues(cdrStream&);
  
  
  static const char* const _user_exns[];

  ::CORBA::String_var arg_0_;
  const char* arg_0;
  ::CORBA::String_var arg_1;
};

void _0RL_cd_7000e62c77f89b95_40000000::marshalArguments(cdrStream& _n)
{
  _n.marshalString(arg_0,0);

}

void _0RL_cd_7000e62c77f89b95_40000000::unmarshalArguments(cdrStream& _n)
{
  arg_0_ = _n.unmarshalString(0);
  arg_0 = arg_0_.in();

}

void _0RL_cd_7000e62c77f89b95_40000000::marshalReturnedValues(cdrStream& _n)
{
  _n.marshalString(arg_1,0);

}

void _0RL_cd_7000e62c77f89b95_40000000::unmarshalReturnedValues(cdrStream& _n)
{
  arg_1 = _n.unmarshalString(0);

}

const char* const _0RL_cd_7000e62c77f89b95_40000000::_user_exns[] = {
  0
};

// Local call call-back function.
static void
_0RL_lcfn_7000e62c77f89b95_50000000(omniCallDescriptor* cd, omniServant* svnt)
{
  _0RL_cd_7000e62c77f89b95_40000000* tcd = (_0RL_cd_7000e62c77f89b95_40000000*)cd;
  First::_impl_IHello* impl = (First::_impl_IHello*) svnt->_ptrToInterface(First::IHello::_PD_repoId);
  impl->SayHello2(tcd->arg_0, tcd->arg_1.out());


}

void First::_objref_IHello::SayHello2(const char* name, ::CORBA::String_out greeting)
{
  _0RL_cd_7000e62c77f89b95_40000000 _call_desc(_0RL_lcfn_7000e62c77f89b95_50000000, "SayHello2", 10);
  _call_desc.arg_0 = name;

  _invoke(_call_desc);
  greeting = _call_desc.arg_1._retn();


}


//
// Code for First::IHello::Message

// Proxy call descriptor class. Mangled signature:
//  _cboolean_n_cstring
class _0RL_cd_7000e62c77f89b95_60000000
  : public omniCallDescriptor
{
public:
  inline _0RL_cd_7000e62c77f89b95_60000000(LocalCallFn lcfn, const char* op_, size_t oplen, _CORBA_Boolean upcall=0)
    : omniCallDescriptor(lcfn, op_, oplen, 0, _user_exns, 0, upcall)
  {
    
  }
  
  void marshalArguments(cdrStream&);
  void unmarshalArguments(cdrStream&);

  void unmarshalReturnedValues(cdrStream&);
  void marshalReturnedValues(cdrStream&);
  
  
  static const char* const _user_exns[];

  ::CORBA::String_var arg_0_;
  char** arg_0;
  ::CORBA::Boolean result;
};

void _0RL_cd_7000e62c77f89b95_60000000::marshalArguments(cdrStream& _n)
{
  _n.marshalString(*arg_0,0);

}

void _0RL_cd_7000e62c77f89b95_60000000::unmarshalArguments(cdrStream& _n)
{
  arg_0_ = _n.unmarshalString(0);
  arg_0 = &arg_0_.inout();

}

void _0RL_cd_7000e62c77f89b95_60000000::marshalReturnedValues(cdrStream& _n)
{
  _n.marshalBoolean(result);
  _n.marshalString(*arg_0,0);

}

void _0RL_cd_7000e62c77f89b95_60000000::unmarshalReturnedValues(cdrStream& _n)
{
  result = _n.unmarshalBoolean();
  arg_0_ = *arg_0;
  *arg_0 = (char*) _CORBA_String_helper::empty_string;
  *arg_0 = _n.unmarshalString(0);

}

const char* const _0RL_cd_7000e62c77f89b95_60000000::_user_exns[] = {
  0
};

// Local call call-back function.
static void
_0RL_lcfn_7000e62c77f89b95_70000000(omniCallDescriptor* cd, omniServant* svnt)
{
  _0RL_cd_7000e62c77f89b95_60000000* tcd = (_0RL_cd_7000e62c77f89b95_60000000*)cd;
  First::_impl_IHello* impl = (First::_impl_IHello*) svnt->_ptrToInterface(First::IHello::_PD_repoId);
  tcd->result = impl->Message(*tcd->arg_0);


}

::CORBA::Boolean First::_objref_IHello::Message(::CORBA::String_INOUT_arg message)
{
  _0RL_cd_7000e62c77f89b95_60000000 _call_desc(_0RL_lcfn_7000e62c77f89b95_70000000, "Message", 8);
  _call_desc.arg_0 = &(char*&) message;

  _invoke(_call_desc);
  return _call_desc.result;


}

First::_pof_IHello::~_pof_IHello() {}


omniObjRef*
First::_pof_IHello::newObjRef(omniIOR* ior, omniIdentity* id)
{
  return new ::First::_objref_IHello(ior, id);
}


::CORBA::Boolean
First::_pof_IHello::is_a(const char* id) const
{
  if (omni::ptrStrMatch(id, ::First::IHello::_PD_repoId))
    return 1;
  
  return 0;
}

const First::_pof_IHello _the_pof_First_mIHello;

First::_impl_IHello::~_impl_IHello() {}


::CORBA::Boolean
First::_impl_IHello::_dispatch(omniCallHandle& _handle)
{
  const char* op = _handle.operation_name();

  if (omni::strMatch(op, "AddValue")) {

    _0RL_cd_7000e62c77f89b95_00000000 _call_desc(_0RL_lcfn_7000e62c77f89b95_10000000, "AddValue", 9, 1);
    
    _handle.upcall(this,_call_desc);
    return 1;
  }

  if (omni::strMatch(op, "SayHello")) {

    _0RL_cd_7000e62c77f89b95_20000000 _call_desc(_0RL_lcfn_7000e62c77f89b95_30000000, "SayHello", 9, 1);
    
    _handle.upcall(this,_call_desc);
    return 1;
  }

  if (omni::strMatch(op, "SayHello2")) {

    _0RL_cd_7000e62c77f89b95_40000000 _call_desc(_0RL_lcfn_7000e62c77f89b95_50000000, "SayHello2", 10, 1);
    
    _handle.upcall(this,_call_desc);
    return 1;
  }

  if (omni::strMatch(op, "Message")) {

    _0RL_cd_7000e62c77f89b95_60000000 _call_desc(_0RL_lcfn_7000e62c77f89b95_70000000, "Message", 8, 1);
    
    _handle.upcall(this,_call_desc);
    return 1;
  }


  return 0;
}

void*
First::_impl_IHello::_ptrToInterface(const char* id)
{
  if (id == ::First::IHello::_PD_repoId)
    return (::First::_impl_IHello*) this;
  
  if (id == ::CORBA::Object::_PD_repoId)
    return (void*) 1;

  if (omni::strMatch(id, ::First::IHello::_PD_repoId))
    return (::First::_impl_IHello*) this;
  
  if (omni::strMatch(id, ::CORBA::Object::_PD_repoId))
    return (void*) 1;
  return 0;
}

const char*
First::_impl_IHello::_mostDerivedRepoId()
{
  return ::First::IHello::_PD_repoId;
}

POA_First::IHello::~IHello() {}

