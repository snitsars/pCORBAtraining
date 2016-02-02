using System;
using System.Diagnostics;
using System.Threading.Tasks;

namespace ProcessRuner
{
    /// <summary>
    ///     Shell for the sample.
    /// </summary>
    public class ProcessLauncher
    {
        public string ApplicationPath { get; set; }
        public bool ExitCode { get; set; }

        private readonly object _thisLock = new object();

        /// <summary>
        ///     Uses the ProcessStartInfo class to start new processes
        ///     mode.
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
                var startInfo = new ProcessStartInfo(ApplicationPath)
                {
                    CreateNoWindow = true,
                    WindowStyle = ProcessWindowStyle.Normal,
                    UseShellExecute = true
                };
                // false;

                //startInfo.Arguments = "www.northwindtraders.com";

                // Start the process.

                myProcess = Process.Start(startInfo);
                // Display the process statistics until
                // the user closes the program.
                do
                {
                    if (myProcess != null && !myProcess.HasExited)
                    {
                        // Refresh the current process property values.
                        myProcess.Refresh();
                        lock (_thisLock)
                        {
                            Console.WriteLine();

                            // Display current process statistics.

                            Console.WriteLine("{0} -", myProcess);
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

                            Console.WriteLine(myProcess.Responding ? "Status = Running" : "Status = Not Responding");
                        }
                    }
                } while (myProcess != null && !myProcess.WaitForExit(1000));

                lock (_thisLock)
                {
                    Console.BackgroundColor = myProcess.ExitCode == 0 ? ConsoleColor.DarkGreen : ConsoleColor.DarkRed;
                    ExitCode = myProcess.ExitCode == 0 ? true : false;

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
                var Server = new ProcessLauncher();
                Server.ApplicationPath = "..\\..\\..\\Servers\\Sharp\\bin\\Debug\\Server.exe";
                var taskServer = new Task(Server.OpenWithExtentionInfo);
                taskServer.Start();

                var Client = new ProcessLauncher();
                Client.ApplicationPath = "..\\..\\..\\Clients\\Sharp\\bin\\Debug\\ClientApp.exe";
                var taskClient = new Task(Client.OpenWithExtentionInfo);
                taskClient.Start();

                return true;
            }
        }

        public static void Main()
        {
            // Get the path that stores favorite links.
            var myFavoritesPath =
                Environment.GetFolderPath(Environment.SpecialFolder.Favorites);
            Tests.Test1();
            Console.ReadLine();
        }
    }
}
