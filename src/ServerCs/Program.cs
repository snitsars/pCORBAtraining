using System;
using System.Runtime.Remoting;
using System.Runtime.Remoting.Channels;
using System.Threading;
using Ch.Elca.Iiop;
using Ch.Elca.Iiop.Idl;
using Ch.Elca.Iiop.Services;
using omg.org.CosNaming;

namespace Org.Uneta.Iiopnet.Examples.First
{
    [SupportedInterface(typeof(IHello))]
    public class HelloImplementation : MarshalByRefObject, IHello
    {
        public override object InitializeLifetimeService()
        {
            return null;
        }
        
        public int AddValue(int a, int b)
        {
            return a + b;
        }

        [return: StringValue][return: WideChar(true)]
        public string SayHello([StringValue][WideChar(true)] string name)
        {
            return "Hello, " + name + ". It's Bob.";
        }


        public void SayHello2([StringValue][WideChar(false)] string name, [StringValue][WideChar(false)] out string greeting)
        {
            greeting = "Hello, " + name + ". It's Bob.";
        }

        public bool Message([StringValue][WideChar(false)] ref string message)
        {
            if (message == "Hello, Bob")
            {
                message = "Hello, Andy.";
                return true;
            }
            return false;
        }
    }

    public class FirstServer
    {
        [STAThread]
        public static void Main(string[] args)
        {
            string host = args[0];
            int port = Int32.Parse(args[1]);

            IiopChannel channel = new IiopChannel(1111);
            ChannelServices.RegisterChannel(channel, false);

            HelloImplementation helloImplementation = new HelloImplementation();
            RemotingServices.Marshal(helloImplementation, "testService");

            CorbaInit init = CorbaInit.GetInit();
            NamingContext nameService = init.GetNameService(host, port);
            
            NameComponent[] name = new NameComponent[] { new NameComponent("testService") };
            nameService.rebind(name, helloImplementation);

            Console.WriteLine("Server ready to use.");
            Thread.Sleep(Timeout.Infinite);
        }
    }
}