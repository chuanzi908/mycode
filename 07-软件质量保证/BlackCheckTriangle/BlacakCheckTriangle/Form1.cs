using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Text.RegularExpressions;

namespace BlacakCheckTriangle
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            //等腰，等边，直角，钝角，锐角。
            Dictionary<String, int> result = new Dictionary<String, int>();
            result.Add("等腰", 0);
            result.Add("等边", 0);
            var t1 = textBox1.Text;
            var t2 = textBox2.Text;
            var t3 = textBox3.Text;
            if (CheckInput(t1, t2, t3))
            {
                var e1 = double.Parse(textBox1.Text);
                var e2 = double.Parse(textBox2.Text);
                var e3 = double.Parse(textBox3.Text);
                double[] Numbers = new double[] { e1, e2, e3 };
                double powSum = Math.Pow(e1, 2) + Math.Pow(e2, 2) + Math.Pow(e3, 2);
                double max = Numbers.Max();
                if (Check1(e1, e2, e3))
                {
                    //三角形。
                    result["等腰"] = Check2(e1, e2, e3) ? 1 : 0;
                    result["等边"] = Check3(e1, e2, e3) ? 1 : 0;        
                    string resultTip = result["等腰"] == 1 ? "等腰" : "";
                    resultTip += result["等边"] == 1 ? "等边" : "";               
                    resultTip += "三角形";
                    MessageBox.Show(resultTip);
                }
                else
                {
                    //不是三角形。
                    MessageBox.Show("您输入的三边构不成三角形！");
                }
            }
            else
            {
                //输入非法。
                MessageBox.Show("您输入的信息有问题！");
            }

        }

        private bool CheckInput(string edge1, string edge2, string edge3)
        {
            bool result = false;
            Regex reg = new Regex("^[0-9]*$");
            if (reg.IsMatch(edge1) && reg.IsMatch(edge2) && reg.IsMatch(edge3))
            {
                if (Int32.Parse(edge1) > 0 && Int32.Parse(edge2) > 0 && Int32.Parse(edge3) > 0)
                {
                    result = true;
                }
            }
            return result;
        }

        private bool Check3(double e1, double e2, double e3)
        {
            return (e1 == e2 && e2 == e3) ? true : false;
        }

        private bool Check2(double e1, double e2, double e3)
        {
            return (e1 == e2 || e2 == e3 || e3 == e1) ? true : false;
        }

        private bool Check1(double edge1, double edge2, double edge3)
        {
            double[] edges = new double[] { edge1, edge2, edge3 };
            double sum = edges[0] + edges[1] + edges[2];
            int succFlag = 0;
            for (int i = 0; i < edges.Count(); i++)
            {
                if (edges[i] < sum - edges[i])
                {
                    succFlag++;
                }
            }
            if (succFlag == 3)
            {
                return true;
            }
            else
            {
                return false;
            }
        }
    
    }
}
