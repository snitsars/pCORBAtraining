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
            int result = -1;
            try
            {
                // Адрес CORBA-сервера.
                const string serverHost = "localhost";
                const int serverPort = 1234;

                // Запрашиваем имя пользователя.
                Console.WriteLine("Enter your name please: ");
                string userName = Console.ReadLine();

                // Регистрируем канал IIOP.
                IiopClientChannel channel = new IiopClientChannel();
                ChannelServices.RegisterChannel(channel);

                // Адрес CORBA-сервера.
                string addressString = "iiop://localhost:1234/hello";
                // Получаем ссылку на клиентский прокси.
                IHello hello = (IHello)RemotingServices.Connect(typeof(IHello), addressString);
                
                // Вызываем CORBA-метод.
                string serverResponse = hello.SayHello(userName);
                //serverResponse = hello.AddVAlue(5,10);
                // Выводим ответ.
                Console.WriteLine("Server ansver is: " + serverResponse);
                Console.ReadLine();
                result = 0;
            } 
            catch (Exception e)
            {
                Console.WriteLine("Exception was raised: " + e);
            }
            return result;
        }
    }
}

