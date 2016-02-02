using System;
using System.Runtime.Remoting;
using System.Runtime.Remoting.Channels;
using System.Threading;
using Ch.Elca.Iiop;

namespace Org.Uneta.Iiopnet.Examples.First
{
    public class HelloImplementation : MarshalByRefObject, IHello
    {
        public override object InitializeLifetimeService()
        {
            // Жизнь не кончается.
            return null;
        }

        public string AddVAlue(int a, int b)
        {
            return Convert.ToString(a + b);
        }

        public string SayHello(string name)
        {
            return "Hello by CORBA, " + name + ".";
        }
    }

    public class FirstServer
    {
        [STAThread]
        public static int Main(string[] args)
        {
            // Регистрируем серверный канал IIOP.
            var serverPort = 1234;
            var channel = new IiopChannel(serverPort);
#pragma warning disable CS0618 // Type or member is obsolete
            ChannelServices.RegisterChannel(channel);
#pragma warning restore CS0618 // Type or member is obsolete

            // Создаем реализацию интерфейса IHello и публикуем её.
            var helloImplementation = new HelloImplementation();
            var objectURI = "hello";
            RemotingServices.Marshal(helloImplementation, objectURI);

            Console.WriteLine("Server ready to use.");
            Thread.Sleep(Timeout.Infinite);
            return 0;
        }
    }
}