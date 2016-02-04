using System;
using System.Runtime.Remoting;
using System.Runtime.Remoting.Channels;
using System.Threading;
using Ch.Elca.Iiop;
using Ch.Elca.Iiop.Idl;

using omg.org.CosNaming;
using Ch.Elca.Iiop.Services;

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
            string host = args[0];
            int port = Int32.Parse(args[1]);

            // Регистрируем серверный канал IIOP.
            int serverPort = 1235;
            IiopChannel channel = new IiopChannel(serverPort);
#pragma warning disable CS0618 // Type or member is obsolete
            ChannelServices.RegisterChannel(channel);
#pragma warning restore CS0618 // Type or member is obsolete

            // Создаем реализацию интерфейса IHello и публикуем её.
            HelloImplementation helloImplementation = new HelloImplementation();
            string objectURI = "testService";
            RemotingServices.Marshal(helloImplementation, objectURI);

            CorbaInit init = CorbaInit.GetInit();
            NamingContext nameService = init.GetNameService(host, port);
            
            NameComponent[] name = new NameComponent[] { new NameComponent("testService") };
            nameService.rebind(name, helloImplementation);

            Console.WriteLine("Server ready to use.");
            Thread.Sleep(Timeout.Infinite);
        }
    }
}