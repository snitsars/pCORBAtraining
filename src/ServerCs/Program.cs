using System;
using System.Runtime.Remoting;
using System.Runtime.Remoting.Channels;
using System.Threading;
using Ch.Elca.Iiop;
using Ch.Elca.Iiop.Idl;

namespace Org.Uneta.Iiopnet.Examples.First
{
    [SupportedInterface(typeof(IHello))]
    public class HelloImplementation : MarshalByRefObject, IHello
    {
        public override object InitializeLifetimeService()
        {
            // Жизнь не кончается.
            return null;
        }
        
        public int AddValue(int a, int b)
        {
            return a + b;
        }

        public string SayHello(string name)
        {
            return "Hello by CORBA, " + name + ".";
        }
    }

    public class FirstServer
    {
        [STAThread]
        public static void Main(string[] args)
        {
            // Регистрируем серверный канал IIOP.
            int serverPort = 1234;
            IiopChannel channel = new IiopChannel(serverPort);
#pragma warning disable CS0618 // Type or member is obsolete
            ChannelServices.RegisterChannel(channel);
#pragma warning restore CS0618 // Type or member is obsolete

            // Создаем реализацию интерфейса IHello и публикуем её.
            HelloImplementation helloImplementation = new HelloImplementation();
            string objectURI = "hello";
            RemotingServices.Marshal(helloImplementation, objectURI);

            Console.WriteLine("Server ready to use.");
            Thread.Sleep(Timeout.Infinite);
        }
    }
}