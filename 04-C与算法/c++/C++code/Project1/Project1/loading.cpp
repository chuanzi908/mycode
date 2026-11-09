//
// 实验一：装载问题 —— 回溯法
// 输入：集装箱个数 n；各集装箱重量 w[1..n]；两艘轮船的载重量 c1、c2
// 输出：每个集装箱的装载结果 x[1..n]（1 装入第一艘船，0 装入第二艘船）
//
#include <iostream>
using namespace std;

const int MAXN = 100;
int n; // 集装箱个数
int w[MAXN]; // 集装箱重量
int c1, c2; // 两艘轮船的载重量
int cw; // 当前已装入第一艘船的重量（current weight）
int bestw; // 第一艘船当前找到的最大装载重量
int r; // 剩余集装箱重量之和
int x[MAXN]; // 当前解向量
int bestx[MAXN]; // 当前最优解向量
long long nodeCnt = 0; // 扩展结点计数（用于观察剪枝效果）

// 递归回溯：搜索第 i 层（i 从 1 开始，表示正在决定第 i 个集装箱的去向）
void BackTrack(int i)
{
	++nodeCnt;
	if (i > n) // 到达叶结点，得到一个完整装载方案
	{
		if (cw > bestw) // 只有装得更满时才更新最优解
		{
			bestw = cw;
			for (int j = 1; j <= n; ++j)
				bestx[j] = x[j];
		}
		return;
	}
	r -= w[i]; // 进入第 i 层，剩余重量中减去 w[i]
}

int main()
{
    cout << "请输入集装箱个数 n：";
    cin >> n;
    cout << "请输入每个集装箱的重量 w1..wn：";
    for (int i = 1; i <= n; ++i) cin >> w[i];
    cout << "请输入两艘轮船的载重量 c1 c2：";
    cin >> c1 >> c2;

    // 初始化
    cw = 0;
    bestw = 0;
    r = 0;
    for (int i = 1; i <= n; ++i) r += w[i];

    // 回溯搜索
    BackTrack(1);

    // 输出结果
    cout << "第一艘船装载的最大重量为：" << bestw << endl;
    cout << "装载方案（1表示装入第一艘船，0表示装入第二艘船）：" << endl;
    for (int i = 1; i <= n; ++i)
        cout << bestx[i] << " ";
    cout << endl;
    cout << "扩展结点数：" << nodeCnt << endl;

    return 0;
}