using System;
using System.Diagnostics;
using System.ComponentModel;
using System.Threading.Tasks;

namespace ProcessRuner
{
    /// <summary>
    /// Shell for the sample.
    /// </summary>
    public class ProcessLauncher
    {
        public string _applicationPath { get; set; }
        
        /// <summary>
        /// Uses the ProcessStartInfo class to start new processes
        /// mode.
        /// </summary>
        public void OpenWithExtentionInfo()
        {
            // Define variables to track the peak
            // memory usage of the process.
            long peakPagedMem = 0,
                peakWorkingSet = 0,
                peakVirtualMem = 0;

            Process myProcess = null;

            try
            {
                ProcessStartInfo startInfo = new ProcessStartInfo(_applicationPath);
                startInfo.WindowStyle = ProcessWindowStyle.Normal;
                startInfo.CreateNoWindow = true;
                startInfo.UseShellExecute = true;// false;

                //startInfo.Arguments = "www.northwindtraders.com";

                // Start the process.

                myProcess = Process.Start(startInfo);
                // Display the process statistics until
                // the user closes the program.
                do
                {
                    if (!myProcess.HasExited)
                    {
                        // Refresh the current process property values.
                        myProcess.Refresh();

                        Console.WriteLine();

                        // Display current process statistics.

                        Console.WriteLine("{0} -", myProcess.ToString());
                        Console.WriteLine("-------------------------------------");
                        Console.WriteLine("  PID: {0}",
                            myProcess.Id);
                        Console.WriteLine("  physical memory usage: {0}",
                            myProcess.WorkingSet64);
                        Console.WriteLine("  base priority: {0}",
                            myProcess.BasePriority);
                        Console.WriteLine("  priority class: {0}",
                            myProcess.PriorityClass);
                        Console.WriteLine("  user processor time: {0}",
                            myProcess.UserProcessorTime);
                        Console.WriteLine("  privileged processor time: {0}",
                            myProcess.PrivilegedProcessorTime);
                        Console.WriteLine("  total processor time: {0}",
                            myProcess.TotalProcessorTime);
                        Console.WriteLine("  PagedSystemMemorySize64: {0}",
                            myProcess.PagedSystemMemorySize64);
                        Console.WriteLine("  PagedMemorySize64: {0}",
                           myProcess.PagedMemorySize64);

                        // Update the values for the overall peak memory statistics.
                        peakPagedMem = myProcess.PeakPagedMemorySize64;
                        peakVirtualMem = myProcess.PeakVirtualMemorySize64;
                        peakWorkingSet = myProcess.PeakWorkingSet64;

                        if (myProcess.Responding)
                        {
                            Console.WriteLine("Status = Running");
                        }
                        else
                        {
                            Console.WriteLine("Status = Not Responding");
                        }
                    }
                }
                while (!myProcess.WaitForExit(1000));

                Console.BackgroundColor = ConsoleColor.DarkRed;
                Console.WriteLine("===============================================");
                Console.WriteLine("Process exit code: {0}",
                    myProcess.ExitCode);

                // Display peak memory statistics for the process.
                Console.WriteLine("Peak physical memory usage of the process: {0}",
                    peakWorkingSet);
                Console.WriteLine("Peak paged memory usage of the process: {0}",
                    peakPagedMem);
                Console.WriteLine("Peak virtual memory usage of the process: {0}",
                    peakVirtualMem);
                Console.WriteLine("===============================================");
                Console.ResetColor();
            }
            finally
            {
                if (myProcess != null)
                {
                    myProcess.Close();
                }
            }
        }

        public static class Tests
        {
            public static bool Test1()
            {
                ProcessLauncher Server = new ProcessLauncher();
                Server._applicationPath = "..\\..\\..\\Servers\\Sharp\\bin\\Debug\\Server.exe";
                Task taskServer = new Task(Server.OpenWithExtentionInfo);
                taskServer.Start();

                ProcessLauncher Client = new ProcessLauncher();
                Client._applicationPath = "..\\..\\..\\Clients\\Sharp\\bin\\Debug\\ClientApp.exe";
                Task taskClient = new Task(Client.OpenWithExtentionInfo);
                taskClient.Start();
                
                return true;
            }

        }



        public static void Main()
        {
            // Get the path that stores favorite links.
            string myFavoritesPath =
            Environment.GetFolderPath(Environment.SpecialFolder.Favorites);
            Tests.Test1();
            Console.ReadLine();
        }
    }
}
