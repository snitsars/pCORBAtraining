using System;
using System.Runtime.Remoting.Channels;
using Ch.Elca.Iiop;
using Ch.Elca.Iiop.Services;
using omg.org.CosNaming;

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

                Console.Write("  AddValue: ");
                check(5 == hello.AddValue(2, 3));

                Console.Write("  SayHello: ");
                check("Hello, Andy. It's Bob." == hello.SayHello("Andy"));

                Console.Write("  SayHello2: ");
                string greeting;
                hello.SayHello2("Andy", out greeting);
                check("Hello, Andy. It's Bob." == greeting);

                Console.Write("  Message: ");
                string message = "Hello, Bob";
                bool responseResult = hello.Message(ref message);
                check(responseResult && ("Hello, Andy." == message));

                /*Console.Write(" Server time: ");
                string strServerTime = "";
                long serverTime = hello.GetServerDateTime(out strServerTime);

                DateTime dtServerTime = DateTime.FromFileTime(serverTime);
                check(strServerTime == dtServerTime.ToString());*/
                
                return result;

            } 
            catch (Exception e)
            {
                Console.WriteLine("Exception was raised: " + e);
            }
            return 0;
        }
    }
}

