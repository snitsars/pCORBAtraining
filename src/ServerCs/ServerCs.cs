using System;
using System.Threading;
using System.Runtime.Remoting.Channels;
using Ch.Elca.Iiop;
using Ch.Elca.Iiop.Services;
using omg.org.CosNaming;
using Org.Uneta.Iiopnet.Examples.First;

namespace ServerCs
{
    public class ServerApp
    {
        static AutoResetEvent shutdownEvent = null;

        private static NamingContext initIIOP(string[] args)
        {
            string host = args[0];
            int nsPort = Int32.Parse(args[1]);
            int callbackPort = Int32.Parse(args[2]);

            ChannelServices.RegisterChannel(new IiopChannel(callbackPort), false);

            CorbaInit init = CorbaInit.GetInit();
            return init.GetNameService(host, nsPort);
        }

        [STAThread]
        public static void Main(string[] args)
        {
            NamingContext nameService = initIIOP(args);

            shutdownEvent = new AutoResetEvent(false);
            HelloImplementation helloImplementation = new HelloImplementation(shutdownEvent);

            nameService.rebind(new NameComponent[] {
                new NameComponent("testService")
            }, helloImplementation);

            shutdownEvent.WaitOne(-1);
        }
    }
}