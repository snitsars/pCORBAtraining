﻿using System;
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
            ProcessStartInfo startInfo = new ProcessStartInfo(app);
            startInfo.WindowStyle = ProcessWindowStyle.Normal;
            startInfo.CreateNoWindow = false;
            startInfo.UseShellExecute = false;
            startInfo.EnvironmentVariables["PATH"] += ";..\\..\\thirdparty\\omniORB-4.2.1\\bin\\x86_win32\\";

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
            Console.Write("ServerCs <-> ClientCs: ");
            ProcessLauncher server = new ProcessLauncher("ServerCs.exe");
            Thread.Sleep(1000);
            ProcessLauncher client = new ProcessLauncher("ClientCs.exe");
            client.wait(3000);
            server.kill();
            
            Console.Write("server_cpp <-> client_cpp: ");
            ProcessLauncher server1 = new ProcessLauncher("..\\Debug_Win32\\server_cpp.exe");
            Thread.Sleep(1000);
            ProcessLauncher client1 = new ProcessLauncher("..\\Debug_Win32\\client_cpp.exe");
            client1.wait(3000);
            server1.kill();

            Console.ReadLine();
        }
    }
}
