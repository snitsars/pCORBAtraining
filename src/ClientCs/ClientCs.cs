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
                try
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

