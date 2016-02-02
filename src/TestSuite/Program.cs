using System;
using System.Diagnostics;
using System.ComponentModel;
using System.Threading.Tasks;

namespace ProcessRuner
{

    public class ProcessLauncher
    {
        Process myProcess = null;

        public ProcessLauncher(string app)
        {
            ProcessStartInfo startInfo = new ProcessStartInfo(app);
            startInfo.WindowStyle = ProcessWindowStyle.Normal;
            startInfo.CreateNoWindow = true;
            startInfo.UseShellExecute = true;// false;

            myProcess = Process.Start(startInfo);
        }

        public void wait(int timeout)
        {
            myProcess.WaitForExit(timeout);

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
            ProcessLauncher client = new ProcessLauncher("ClientCs.exe");
            client.wait(3000);
            server.kill();

            Console.ReadLine();
        }
    }
}
