// MD Viewer launcher: runs mdview.bat (in the same folder) with no black window.
using System;
using System.Diagnostics;
using System.IO;
using System.Reflection;

class MdViewerLauncher
{
    [STAThread]
    static void Main(string[] args)
    {
        if (args.Length == 0) return;
        string dir = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
        string bat = Path.Combine(dir, "mdview.bat");
        ProcessStartInfo psi = new ProcessStartInfo();
        psi.FileName = "cmd.exe";
        psi.Arguments = "/c \"\"" + bat + "\" \"" + args[0] + "\"\"";
        psi.UseShellExecute = false;
        psi.CreateNoWindow = true;
        Process.Start(psi);
    }
}
