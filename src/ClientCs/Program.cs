using System;
using System.Runtime.Remoting.Channels;
using System.Runtime.Remoting;
using Ch.Elca.Iiop;

using omg.org.CosNaming;
using Ch.Elca.Iiop.Services;

namespace Org.Uneta.Iiopnet.Examples.First
{
    class FirstClient
    {
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

                if (5 != hello.AddValue(2, 3)) return -1;

                if ("Hello by CORBA, Andy." != hello.SayHello("Andy")) return -1;
            } 
            catch (Exception e)
            {
                Console.WriteLine("Exception was raised: " + e);
                return -1;
            }
            return 0;
        }
    }
}

