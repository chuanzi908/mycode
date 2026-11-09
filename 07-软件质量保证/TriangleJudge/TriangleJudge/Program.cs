/********************************************************************
* 版权所有 (C)2026, 天津理工大学华信软件学院。
*
* 文件名称：Program.cs
* 文件标识：SQ-LAB1-001
* 内容摘要：程序入口，启动三角形判定窗体。
* 其它说明：对应《软件质量保证与测试》实验一 高质量编程。
* 当前版本：V1.0
* 作    者：王博川
* 完成日期：2026年11月9日
* 修改记录1：
*    修改日期：2026年11月9日
*    版 本 号：V1.0
*    修 改 人：王博川
*    修改内容：首次创建。
**********************************************************************/
using System;
using System.Windows.Forms;

namespace Wbc.SoftwareQuality.Triangle
{
    /// <summary>
    /// 应用程序入口类。
    /// </summary>
    internal static class Program
    {
        /// <summary>
        /// 应用程序的主入口点。
        /// </summary>
        [STAThread]
        private static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new MainForm());
        }
    }
}
