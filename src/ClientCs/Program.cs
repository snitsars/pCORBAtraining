using System;
using System.Runtime.Remoting.Channels;
using System.Runtime.Remoting;
using Ch.Elca.Iiop;

namespace Org.Uneta.Iiopnet.Examples.First
{
    class FirstClient
    {
        [STAThread]
        public static int Main(string[] args)
        {
            try
            {
                // Адрес CORBA-сервера.
                const string serverHost = "localhost";
                const int serverPort = 1234;

                // Регистрируем канал IIOP.
                IiopClientChannel channel = new IiopClientChannel();
                ChannelServices.RegisterChannel(channel);

                // Адрес CORBA-сервера.
                string addressString = "iiop://localhost:1234/hello";
                // Получаем ссылку на клиентский прокси.
                IHello hello = (IHello)RemotingServices.Connect(typeof(IHello), addressString);

                // tests

                if ("5" != hello.AddVAlue(2, 3)) return -1;

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

