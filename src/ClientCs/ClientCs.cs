using System;
using System.Runtime.Remoting.Channels;
using Ch.Elca.Iiop;
using Ch.Elca.Iiop.Services;
using omg.org.CosNaming;
using omg.org.CORBA;
using Org.Uneta.Iiopnet.Examples.First.IHello_package;


namespace Org.Uneta.Iiopnet.Examples.First
{
    class TestCallBack : MarshalByRefObject, ITestCallBack
    {
        private string greeting = null;
        public string Greeting { get { return greeting; } }

        public int _call(int inputValue)
        {
            greeting = "Hello from Server";
            return inputValue+7;
        }
    }

    class ClientApp
    {
        private static int result = 0;
        
        private static void check(bool status)
        {
            if (!status)
            {
                Console.WriteLine("FAILED");
                result = -1;
            }
            else
                Console.WriteLine("OK");
        }

        private static bool equal(MyComplexNumber x, MyComplexNumber y)
        {
            return x.re == y.re && x.im == y.im;
        }

        private static void runTests(IHello hello)
        {
            #region AddValue
            {
                Console.Write("  AddValue: ");
                check(5 == hello.AddValue(2, 3));
            }
            #endregion

            #region SayHello
            {
                Console.Write("  SayHello: ");
                check("Hello, Andy. It's Bob." == hello.SayHello("Andy"));
            }
            #endregion

            #region SayHello2
            {
                Console.Write("  SayHello2: ");
                string greeting;
                hello.SayHello2("Andy", out greeting);
                check("Hello, Andy. It's Bob." == greeting);
            }
            #endregion

            #region Message
            {
                Console.Write("  Message: ");
                string message = "Hello, Bob";
                bool result = hello.Message(ref message);
                check(result && ("Hello, Andy." == message));
            }
            #endregion

            #region MulComplex
            {
                Console.Write("  MulComplex: ");
                MyComplexNumber x = new MyComplexNumber(2, 3);
                MyComplexNumber y = new MyComplexNumber(5, 6);
                MyComplexNumber expected = new MyComplexNumber(x.re * y.re - x.im * y.im, x.re * y.im + x.im - y.re);

                MyComplexNumber result = hello.MulComplex(x, ref y);
                check(equal(result, expected) && equal(result, expected));
            }
            try
            {
                Console.Write("  MulComplexAsAny: ");
                MyComplexNumber x = new MyComplexNumber(2, 3);
                MyComplexNumber y = new MyComplexNumber(5, 6);
                MyComplexNumber expected = new MyComplexNumber(x.re * y.re - x.im * y.im, x.re * y.im + x.im - y.re);


                object result;
                bool success = hello.MulComplexAsAny(x, y, out result);
                MyComplexNumber complexNumber = (MyComplexNumber)result;

                check(success && equal(complexNumber, expected));
            }
            catch (System.Exception)
            {
                Console.WriteLine("__NOT RELEVANT__: Known issue with IIOP.NET marshalling <-> omniORB unmarshsalling of 'Any' type");
            }

            #endregion

            #region TimeTransfer
            {
                Console.Write("  DataTimeTransfer: ");

                DateTime dateTime = new DateTime(2016, 2, 8);
                long dataTimeValue = dateTime.ToFileTimeUtc();

                hello.DataTimeTransfer(ref dataTimeValue);

                DateTime fromServer = DateTime.FromFileTimeUtc(dataTimeValue);
                check(dateTime == fromServer);
            }
            #endregion

            #region Exception hadlers
            Console.WriteLine("  Install exceptions hadlers: Not relevant in iiop.net");
            #endregion

            #region System Exception
            try
            {
                Console.Write("  Catch NO_IMPLEMENT: ");
                hello.ThrowExceptions(0);
            }
            catch (NO_IMPLEMENT se)
            {
                check(1 == se.Minor);
            }
            catch (Exception)
            {
                check(false);
            }
            #endregion

            #region Plain user exception
            try
            {
                Console.Write("  Catch plain user exception: ");
                hello.ThrowExceptions(1);
            }
            catch (UserExceptionS ue)
            {
                check(ue.Message.Contains("UserExceptionS"));
            }
            catch (Exception)
            {
                check(false);
            }
            #endregion

            #region User exception with members
            try
            {
                Console.Write("  Catch user exception with members: ");
                hello.ThrowExceptions(2);
            }
            catch (UserExceptionExt ue)
            {
                check(ue.reason == "EXCEPTIONS_WORKS" && ue.codeError == 254);
            }
            catch (Exception)
            {
                check(false);
            }
            #endregion

            #region Unknown exception
            try
            {
                Console.Write("  Catch unknown exception: ");
                hello.ThrowExceptions(4);
            }
            catch (omg.org.CORBA.UNKNOWN e)
            {
                check(e.Message.Contains("UNKNOWN"));
            }
            catch (Exception)
            {
                check(false);
            }
            #endregion

            #region callback
            try
            {
                Console.WriteLine("  Callback: ");
                TestCallBack callback = new TestCallBack();
                check(hello.CallMe(callback) && callback.Greeting == "Hello from Server");
            }
            catch (Exception)
            {
                check(false);
            }
            #endregion

            #region sequense
            try
            {
                Console.Write("  Sequence reversed: ");
                int[] array = { 1, 3, 5, 7, 10 };
                int[] reversed_arr = hello.Reverse(array);

                check(System.Linq.Enumerable.SequenceEqual(new int[] { 10, 7, 5, 3, 1 }, reversed_arr));
            }
            catch (Exception)
            {
                check(false);
            }
            #endregion

            #region Shutdown
            try
            {
                Console.Write("  Shutdown: ");
                hello.Shutdown();
                check(true);
            }
            catch (Exception)
            {
                check(false);
            }
            #endregion
        }

        private static NamingContext initIIOP(string[] args)
        {
            string host = args[0];
            int nsPort = Int32.Parse(args[1]);
            int callbackPort = Int32.Parse(args[2]);

            ChannelServices.RegisterChannel(new IiopChannel(callbackPort), false);

            CorbaInit init = CorbaInit.GetInit();
            return init.GetNameService(host, nsPort);
        }

        [STAThread]
        public static int Main(string[] args)
        {
            NamingContext nameService = initIIOP(args);

            IHello hello = (IHello)nameService.resolve(new NameComponent[] {
                new NameComponent("testService")
            });

            runTests(hello);

            return result;
        }
    }
}

