using System;
using System.Diagnostics;
using System.ComponentModel;
using System.Threading;

namespace ProcessRuner
{

    public class ProcessLauncher
    {
        Process myProcess = null;

        public ProcessLauncher(string app)
        {
            ProcessStartInfo startInfo = new ProcessStartInfo(app, "localhost 1234");
            startInfo.WindowStyle = ProcessWindowStyle.Normal;
            startInfo.CreateNoWindow = false;
            startInfo.UseShellExecute = false;
            startInfo.EnvironmentVariables["PATH"] += ";..\\..\\thirdparty\\omniORB-4.2.1\\bin\\x86_win32\\";
            startInfo.EnvironmentVariables["OMNIORB_CONFIG"] = "..\\..\\config\\omniORB.cfg";

            myProcess = Process.Start(startInfo);
        }

        public void wait(int timeout)
        {
            if (!myProcess.WaitForExit(timeout))
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("FAILED");
                Console.ResetColor();
            }
            else
            {
                if (myProcess.ExitCode != 0)
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

        public void kill()
        {
            myProcess.Kill();
        }

    }

    class ProcessRuner
    {
        
        public static void Main()
        {
            Console.WriteLine("ClientCs -> ServerCs");
            ProcessLauncher server = new ProcessLauncher("ServerCs.exe");
            Thread.Sleep(1000);
            ProcessLauncher client = new ProcessLauncher("ClientCs.exe");
            client.wait(3000);
            server.kill();
            
            Console.WriteLine("client_cpp -> server_cpp");
            ProcessLauncher server1 = new ProcessLauncher("..\\Debug_Win32\\server_cpp.exe");
            Thread.Sleep(1000);
            ProcessLauncher client1 = new ProcessLauncher("..\\Debug_Win32\\client_cpp.exe");
            client1.wait(3000);
            server1.kill();
            
            Console.WriteLine("client_cpp -> ServerCs");
            ProcessLauncher server2 = new ProcessLauncher("ServerCs.exe");
            Thread.Sleep(1000);
            ProcessLauncher client2 = new ProcessLauncher("..\\Debug_Win32\\client_cpp.exe");
            client2.wait(3000);
            server2.kill();

            Console.WriteLine("ClientCs -> server_cpp");
            ProcessLauncher server3 = new ProcessLauncher("..\\Debug_Win32\\server_cpp.exe");
            Thread.Sleep(1000);
            ProcessLauncher client3 = new ProcessLauncher("ClientCs.exe");
            client3.wait(3000);
            server3.kill();

            Console.Write("Press enter"); Console.ReadLine();
        }
    }
}
