using System;
using System.Diagnostics;
using System.ComponentModel;
using System.Threading;

namespace TestSuite
{
    public class Test
    {
        private Process mClientProcess = null;
        private Process mServerProcess = null;

        public Test(string client, string clientParams, string server, string serverParams)
        {
            Console.WriteLine("\n" + client + " -> " + server);

            mServerProcess = StartProcess(server, serverParams);
            Thread.Sleep(1000);
            mClientProcess = StartProcess(client, clientParams);
            wait(10000);
        }

        private Process StartProcess(string app, string param)
        {
            ProcessStartInfo startInfo = new ProcessStartInfo(app, param);
            startInfo.WindowStyle = ProcessWindowStyle.Normal;
            startInfo.CreateNoWindow = false;
            startInfo.UseShellExecute = false;
            startInfo.EnvironmentVariables["PATH"] += ";..\\..\\thirdparty\\omniORB-4.2.1\\bin\\x86_win32\\";
            startInfo.EnvironmentVariables["OMNIORB_CONFIG"] = "..\\..\\config\\omniORB.cfg";

            return Process.Start(startInfo);
        }

        private void wait(int timeout)
        {
            if (!mClientProcess.WaitForExit(timeout))
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("FAILED");
                Console.ResetColor();
            }
            else
            {
                if (mClientProcess.ExitCode != 0)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine("FAILED");
                    Console.ResetColor();
                }
                else
                {
                    Console.ForegroundColor = ConsoleColor.Green;
                    Console.WriteLine("OK");
                    Console.ResetColor();
                }
            }
        }
    }

    class TestSuiteApp
    {
        public static void Main()
        {
            Test t1 = new Test("ClientCs.exe",                      "localhost 1234 1235",  "ServerCs.exe",                     "localhost 1234 1236");
            Test t2 = new Test("..\\Debug_Win32\\client_cpp.exe",   "",                     "..\\Debug_Win32\\server_cpp.exe",  "");
            Test t3 = new Test("ClientCs.exe",                      "localhost 1234 1235",  "..\\Debug_Win32\\server_cpp.exe",  "");
            Test t4 = new Test("..\\Debug_Win32\\client_cpp.exe",   "",                     "ServerCs.exe",                     "localhost 1234 1236");

            Console.Write("Press enter");
            Console.Read();
        }
    }
}
