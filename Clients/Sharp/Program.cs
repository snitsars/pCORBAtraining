using System;
using System.Runtime.Remoting;
using System.Runtime.Remoting.Channels;
using System.Threading;
using Ch.Elca.Iiop;

namespace Org.Uneta.Iiopnet.Examples.First
{
    internal class FirstClient
    {
        [STAThread]
        public static int Main(string[] args)
        {
            var result = -1;
            try
            {
                // Адрес CORBA-сервера.
                const string serverHost = "localhost";
                const int serverPort = 1234;

                // Запрашиваем имя пользователя.
                Console.WriteLine("Enter your name please: ");

                // Регистрируем канал IIOP.
                var channel = new IiopClientChannel();
                ChannelServices.RegisterChannel(channel);

                // Адрес CORBA-сервера.
                var addressString = "iiop://localhost:1234/hello";
                // Получаем ссылку на клиентский прокси.
                var hello = (IHello) RemotingServices.Connect(typeof (IHello), addressString);

                // Вызываем CORBA-метод.
                string serverResponse = hello.SayHello(Environment.UserName);
                //serverResponse = hello.AddVAlue(5,10);
                // Выводим ответ.
                Console.WriteLine("Server ansver is: " + serverResponse);
                Thread.Sleep(1000);
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