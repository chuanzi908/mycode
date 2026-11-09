/********************************************************************
* 版权所有 (C)2026, 天津理工大学华信软件学院。
*
* 文件名称：MainForm.cs
* 文件标识：SQ-LAB1-007
* 内容摘要：主窗体逻辑，负责界面输入的读取、校验与结果显示。
* 其它说明：业务判定委托给 ITriangleClassifier，界面层不含算法细节。
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
using System.Drawing;
using System.Windows.Forms;
using Wbc.SoftwareQuality.Triangle.Models;
using Wbc.SoftwareQuality.Triangle.Services;

namespace Wbc.SoftwareQuality.Triangle
{
    /// <summary>
    /// 三角形判定的主窗体。
    /// </summary>
    public partial class MainForm : Form
    {
        /// <summary>
        /// 判定成功时的结果文字颜色。
        /// </summary>
        private static readonly Color SuccessColor = Color.FromArgb(20, 83, 79);

        /// <summary>
        /// 判定失败时的结果文字颜色。
        /// </summary>
        private static readonly Color FailureColor = Color.FromArgb(192, 0, 0);

        /// <summary>
        /// 三角形判定服务。
        /// </summary>
        private readonly ITriangleClassifier mClassifier = new TriangleClassifier();

        /// <summary>
        /// 初始化窗体。
        /// </summary>
        public MainForm()
        {
            InitializeComponent();
        }

        /// <summary>
        /// 点击“判定”按钮时执行的处理。
        /// </summary>
        /// <param name="sender">事件源。</param>
        /// <param name="e">事件参数。</param>
        private void BtnJudge_Click(object sender, EventArgs e)
        {
            if (!mClassifier.TryParseEdge(txtEdgeA.Text, out int edgeA))
            {
                ShowMessage("边 A 必须是不小于 1 的整数。", FailureColor);
                txtEdgeA.Focus();
                txtEdgeA.SelectAll();
                return;
            }

            if (!mClassifier.TryParseEdge(txtEdgeB.Text, out int edgeB))
            {
                ShowMessage("边 B 必须是不小于 1 的整数。", FailureColor);
                txtEdgeB.Focus();
                txtEdgeB.SelectAll();
                return;
            }

            if (!mClassifier.TryParseEdge(txtEdgeC.Text, out int edgeC))
            {
                ShowMessage("边 C 必须是不小于 1 的整数。", FailureColor);
                txtEdgeC.Focus();
                txtEdgeC.SelectAll();
                return;
            }

            TriangleType triangleType = mClassifier.Classify(edgeA, edgeB, edgeC);
            ShowMessage(DescribeTriangle(triangleType, edgeA, edgeB, edgeC),
                triangleType == TriangleType.NotTriangle ? FailureColor : SuccessColor);
        }

        /// <summary>
        /// 点击“清空”按钮时执行的处理。
        /// </summary>
        /// <param name="sender">事件源。</param>
        /// <param name="e">事件参数。</param>
        private void BtnClear_Click(object sender, EventArgs e)
        {
            txtEdgeA.Clear();
            txtEdgeB.Clear();
            txtEdgeC.Clear();
            ShowMessage("请输入三条边的长度（正整数）", Color.Black);
            txtEdgeA.Focus();
        }

        /// <summary>
        /// 根据三角形类型生成提示文字。
        /// </summary>
        /// <param name="triangleType">三角形类型。</param>
        /// <param name="edgeA">第一条边。</param>
        /// <param name="edgeB">第二条边。</param>
        /// <param name="edgeC">第三条边。</param>
        /// <returns>用于界面显示的提示文字。</returns>
        private static string DescribeTriangle(TriangleType triangleType, int edgeA, int edgeB, int edgeC)
        {
            string edgeText = string.Format("（{0}, {1}, {2}）", edgeA, edgeB, edgeC);

            switch (triangleType)
            {
                case TriangleType.Equilateral:
                    return "这是等边三角形" + edgeText + "。";
                case TriangleType.Isosceles:
                    return "这是等腰三角形" + edgeText + "。";
                case TriangleType.Scalene:
                    return "这是普通三角形" + edgeText + "。";
                default:
                    return "这三条边不能构成三角形" + edgeText + "。";
            }
        }

        /// <summary>
        /// 在结果标签上显示文字并设置颜色。
        /// </summary>
        /// <param name="message">提示文字。</param>
        /// <param name="color">文字颜色。</param>
        private void ShowMessage(string message, Color color)
        {
            lblResult.Text = message;
            lblResult.ForeColor = color;
        }
    }
}
