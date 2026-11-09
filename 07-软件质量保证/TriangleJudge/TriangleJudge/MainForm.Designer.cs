/********************************************************************
* 版权所有 (C)2026, 天津理工大学华信软件学院。
*
* 文件名称：MainForm.Designer.cs
* 文件标识：SQ-LAB1-006
* 内容摘要：窗体设计器代码，定义三个输入框、判定按钮与结果标签。
* 其它说明：控件命名遵循规范中的组件缩写表（lbl/txt/btn）。
* 当前版本：V1.0
* 作    者：王博川
* 完成日期：2026年11月9日
* 修改记录1：
*    修改日期：2026年11月9日
*    版 本 号：V1.0
*    修 改 人：王博川
*    修改内容：首次创建。
**********************************************************************/
namespace Wbc.SoftwareQuality.Triangle
{
    /// <summary>
    /// 主窗体。
    /// </summary>
    partial class MainForm
    {
        /// <summary>
        /// 设计器所需的组件容器。
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 标题标签。
        /// </summary>
        private System.Windows.Forms.Label lblTitle;

        /// <summary>
        /// 第一条边的说明标签。
        /// </summary>
        private System.Windows.Forms.Label lblEdgeA;

        /// <summary>
        /// 第二条边的说明标签。
        /// </summary>
        private System.Windows.Forms.Label lblEdgeB;

        /// <summary>
        /// 第三条边的说明标签。
        /// </summary>
        private System.Windows.Forms.Label lblEdgeC;

        /// <summary>
        /// 第一条边的输入框。
        /// </summary>
        private System.Windows.Forms.TextBox txtEdgeA;

        /// <summary>
        /// 第二条边的输入框。
        /// </summary>
        private System.Windows.Forms.TextBox txtEdgeB;

        /// <summary>
        /// 第三条边的输入框。
        /// </summary>
        private System.Windows.Forms.TextBox txtEdgeC;

        /// <summary>
        /// 判定按钮。
        /// </summary>
        private System.Windows.Forms.Button btnJudge;

        /// <summary>
        /// 清空按钮。
        /// </summary>
        private System.Windows.Forms.Button btnClear;

        /// <summary>
        /// 结果显示标签。
        /// </summary>
        private System.Windows.Forms.Label lblResult;

        /// <summary>
        /// 释放设计器使用的资源。
        /// </summary>
        /// <param name="disposing">为 true 时释放托管资源。</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }

            base.Dispose(disposing);
        }

        /// <summary>
        /// 初始化窗体控件。
        /// </summary>
        private void InitializeComponent()
        {
            this.lblTitle = new System.Windows.Forms.Label();
            this.lblEdgeA = new System.Windows.Forms.Label();
            this.lblEdgeB = new System.Windows.Forms.Label();
            this.lblEdgeC = new System.Windows.Forms.Label();
            this.txtEdgeA = new System.Windows.Forms.TextBox();
            this.txtEdgeB = new System.Windows.Forms.TextBox();
            this.txtEdgeC = new System.Windows.Forms.TextBox();
            this.btnJudge = new System.Windows.Forms.Button();
            this.btnClear = new System.Windows.Forms.Button();
            this.lblResult = new System.Windows.Forms.Label();
            this.SuspendLayout();
            //
            // lblTitle
            //
            this.lblTitle.AutoSize = true;
            this.lblTitle.Font = new System.Drawing.Font("微软雅黑", 14F, System.Drawing.FontStyle.Bold);
            this.lblTitle.Location = new System.Drawing.Point(20, 15);
            this.lblTitle.Name = "lblTitle";
            this.lblTitle.Size = new System.Drawing.Size(200, 31);
            this.lblTitle.TabIndex = 0;
            this.lblTitle.Text = "三角形形状判定";
            //
            // lblEdgeA
            //
            this.lblEdgeA.AutoSize = true;
            this.lblEdgeA.Location = new System.Drawing.Point(20, 66);
            this.lblEdgeA.Name = "lblEdgeA";
            this.lblEdgeA.Size = new System.Drawing.Size(52, 17);
            this.lblEdgeA.TabIndex = 1;
            this.lblEdgeA.Text = "边 A：";
            //
            // txtEdgeA
            //
            this.txtEdgeA.Location = new System.Drawing.Point(110, 62);
            this.txtEdgeA.Name = "txtEdgeA";
            this.txtEdgeA.Size = new System.Drawing.Size(140, 27);
            this.txtEdgeA.TabIndex = 2;
            //
            // lblEdgeB
            //
            this.lblEdgeB.AutoSize = true;
            this.lblEdgeB.Location = new System.Drawing.Point(20, 108);
            this.lblEdgeB.Name = "lblEdgeB";
            this.lblEdgeB.Size = new System.Drawing.Size(52, 17);
            this.lblEdgeB.TabIndex = 3;
            this.lblEdgeB.Text = "边 B：";
            //
            // txtEdgeB
            //
            this.txtEdgeB.Location = new System.Drawing.Point(110, 104);
            this.txtEdgeB.Name = "txtEdgeB";
            this.txtEdgeB.Size = new System.Drawing.Size(140, 27);
            this.txtEdgeB.TabIndex = 4;
            //
            // lblEdgeC
            //
            this.lblEdgeC.AutoSize = true;
            this.lblEdgeC.Location = new System.Drawing.Point(20, 150);
            this.lblEdgeC.Name = "lblEdgeC";
            this.lblEdgeC.Size = new System.Drawing.Size(52, 17);
            this.lblEdgeC.TabIndex = 5;
            this.lblEdgeC.Text = "边 C：";
            //
            // txtEdgeC
            //
            this.txtEdgeC.Location = new System.Drawing.Point(110, 146);
            this.txtEdgeC.Name = "txtEdgeC";
            this.txtEdgeC.Size = new System.Drawing.Size(140, 27);
            this.txtEdgeC.TabIndex = 6;
            //
            // btnJudge
            //
            this.btnJudge.Location = new System.Drawing.Point(23, 195);
            this.btnJudge.Name = "btnJudge";
            this.btnJudge.Size = new System.Drawing.Size(105, 34);
            this.btnJudge.TabIndex = 7;
            this.btnJudge.Text = "判 定";
            this.btnJudge.UseVisualStyleBackColor = true;
            this.btnJudge.Click += new System.EventHandler(this.BtnJudge_Click);
            //
            // btnClear
            //
            this.btnClear.Location = new System.Drawing.Point(145, 195);
            this.btnClear.Name = "btnClear";
            this.btnClear.Size = new System.Drawing.Size(105, 34);
            this.btnClear.TabIndex = 8;
            this.btnClear.Text = "清 空";
            this.btnClear.UseVisualStyleBackColor = true;
            this.btnClear.Click += new System.EventHandler(this.BtnClear_Click);
            //
            // lblResult
            //
            this.lblResult.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.lblResult.Font = new System.Drawing.Font("微软雅黑", 10.5F);
            this.lblResult.Location = new System.Drawing.Point(23, 245);
            this.lblResult.Name = "lblResult";
            this.lblResult.Size = new System.Drawing.Size(420, 45);
            this.lblResult.TabIndex = 9;
            this.lblResult.Text = "请输入三条边的长度（正整数）";
            this.lblResult.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            //
            // MainForm
            //
            this.AcceptButton = this.btnJudge;
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 17F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(470, 310);
            this.Controls.Add(this.lblResult);
            this.Controls.Add(this.btnClear);
            this.Controls.Add(this.btnJudge);
            this.Controls.Add(this.txtEdgeC);
            this.Controls.Add(this.lblEdgeC);
            this.Controls.Add(this.txtEdgeB);
            this.Controls.Add(this.lblEdgeB);
            this.Controls.Add(this.txtEdgeA);
            this.Controls.Add(this.lblEdgeA);
            this.Controls.Add(this.lblTitle);
            this.Font = new System.Drawing.Font("微软雅黑", 9F);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.MaximizeBox = false;
            this.Name = "MainForm";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "三角形形状判定 - 软件质量保证与测试实验一";
            this.ResumeLayout(false);
            this.PerformLayout();
        }
    }
}
