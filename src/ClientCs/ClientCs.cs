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
        public string getDecoratedString(string input)
        {
            try
            {
                return input + "  attached with DateTime " + DateTime.Now.ToString();
            }
            catch (Exception)
            {
                return string.Empty;
            }
        }
    }

    class FirstClient
    {
        private static int _result = 0;
        
        private static void check(bool status)
        {
            if (!status)
            {
                Console.WriteLine("FAILED");
                _result = -1;
            }
            else
                Console.WriteLine("OK");
        }

        private static bool equal(MyComplexNumber x, MyComplexNumber y)
        {
            return x.re == y.re && x.im == y.im;
        }

        [STAThread]
        public static int Main(string[] args)
        {
            try
            {
                string host = args[0];
                int port = Int32.Parse(args[1]);
                int callbackPort = Int32.Parse(args[2]);

                // Регистрируем канал IIOP.
                var chanel = new IiopChannel(callbackPort);
                //IiopClientChannel channel = new IiopClientChannel();
                ChannelServices.RegisterChannel(chanel, false);

                CorbaInit init = CorbaInit.GetInit();
                NamingContext nameService = init.GetNameService(host, port);

                NameComponent[] name = new NameComponent[] { new NameComponent("testService") };

                // Получаем ссылку на клиентский прокси.
                IHello hello = (IHello)nameService.resolve(name);

                var calback = new TestCallBack();
                hello.setCallBack(calback);

                // tests
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
                catch(System.Exception e)
                {
                    check(false);
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

                #region ThrowExceptions
                {
                    Console.WriteLine("  Install exceptions hadlers: Not relevant in iiop.net");

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

                    try
                    {
                        Console.Write("  Catch unknown exception: ");
                        hello.ThrowExceptions(4);
                    }
                    catch (omg.org.CORBA.UNKNOWN e)
                    {
                        check(e.Message.Contains("UNKNOWN"));
                    }
                    catch(Exception)
                    {
                        check(false);
                    }

                }
                #endregion
                #region callbackCall

                {
                    //string result = hello.callCallBack().getDecoratedString("Hello world");
                    //Console.WriteLine(" Decorated String: " + result);
                }
                #endregion

                #region sequense
                try
                {
                    Console.Write("  Sequence reversed: ");
                    int[] array = {1, 3, 5, 7, 10};
                    int[] reversed_arr = hello.Reverse(array);

                    check(System.Linq.Enumerable.SequenceEqual(new int[]{10, 7, 5, 3, 1}, reversed_arr));

                }
                catch(Exception)
                {
                    check(false);
                }
                return FirstClient._result;
                #endregion

            }
            catch (Exception e)
            {
                Console.WriteLine("Exception was raised: " + e);
            }
            return 0;
        }
    }
}

