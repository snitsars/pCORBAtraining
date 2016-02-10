using System;
using System.Runtime.Remoting.Channels;
using Ch.Elca.Iiop;
using Ch.Elca.Iiop.Services;
using omg.org.CosNaming;
using omg.org.CORBA;
using Org.Uneta.Iiopnet.Examples.First.IHello_package;

namespace Org.Uneta.Iiopnet.Examples.First
{
    class FirstClient
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

        [STAThread]
        public static int Main(string[] args)
        {
            try
            {
                string host = args[0];
                int port = Int32.Parse(args[1]);

                // Регистрируем канал IIOP.
                IiopClientChannel channel = new IiopClientChannel();
                ChannelServices.RegisterChannel(channel, false);

                CorbaInit init = CorbaInit.GetInit();
                NamingContext nameService = init.GetNameService(host, port);

                NameComponent[] name = new NameComponent[] { new NameComponent("testService") };

                // Получаем ссылку на клиентский прокси.
                IHello hello = (IHello)nameService.resolve(name);

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
                {
                    Console.Write("  MulComplexAsAny: ");
                    MyComplexNumber x = new MyComplexNumber(2, 3);
                    MyComplexNumber y = new MyComplexNumber(5, 6);
                    MyComplexNumber expected = new MyComplexNumber(x.re * y.re - x.im * y.im, x.re * y.im + x.im - y.re);


                    object _result;
                    bool success = hello.MulComplexAsAny(x, y, out _result);
                    MyComplexNumber result = (MyComplexNumber)_result;

                    check(success && equal(result, expected));
                }
                #endregion

                #region TimeTransfer
                {
                    Console.Write(" DataTimeTransfer: ");
                    string initialValue = "08/02/2016 00:00:00.00";
                    DateTime dateTime = Convert.ToDateTime(initialValue);
                    long dataTimeValue = dateTime.ToFileTimeUtc();

                    hello.DataTimeTransfer(ref dataTimeValue);

                    DateTime fromServer = DateTime.FromFileTimeUtc(dataTimeValue);
                    check(dateTime == fromServer);
                }
                #endregion

                #region ThrowExceptions
                {
                    Console.WriteLine(" ThrowExceptions: ");
                    try
                    {
                        hello.ThrowExceptions(0);
                    }
                    catch (NO_IMPLEMENT se)
                    {
                        Console.Write("   NO_IMPLEMENT: ");
                        check(1 == se.Minor);
                    }

                    try
                    {
                        hello.ThrowExceptions(1);
                    }
                    catch (UserExceptionS ue)
                    {
                        Console.Write("   UserExceptionS: ");
                        check(ue.Message.Contains("UserExceptionS"));
                    }
                    try
                    {
                        hello.ThrowExceptions(2);
                    }
                    catch (UserExceptionExt ue)
                    {
                        Console.Write("   UserExceptionExt: ");
                        var checkValue = ue.reason;
                        checkValue = checkValue + ue.codeError;                        
                        check("EXCEPTIONS_WORKS254" == checkValue);
                    }
                    try
                    {
                        hello.ThrowExceptions(4);
                    }
                    catch (Exception e)
                    {
                        Console.Write("   C# NotImplementedException: ");
                        check(e.Message.Contains("UNKNOWN"));
                    }

                }
                #endregion

                return FirstClient.result;

            }
            catch (Exception e)
            {
                Console.WriteLine("Exception was raised: " + e);
            }
            return 0;
        }
    }
}

