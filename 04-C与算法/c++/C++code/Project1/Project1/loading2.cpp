源程序（Wiring.cpp）
//
// 实验三：布线问题 —— 分支限界法（队列式）
// 输入：阵列规模 n；n 行 n 列布线阵列（0 可布线，1 已封锁）；
// 起点 a(r,c)、终点 b(r,c)（行列均从 1 开始）
// 输出：a 到 b 的最短布线长度，以及一条最短布线路径
//
#include <iostream>
#include <queue>
#include <sstream>
using namespace std;

const int MAXN = 50;
struct Position { // 方格坐标
	int row, col;
};
int n; // 阵列规模
int grid[MAXN][MAXN]; // 0 可布线，1 已封锁
Position a, b; // 起点、终点
int dist[MAXN][MAXN]; // 起点到各方格的最短布线长度，-1 表示不可达
Position from[MAXN][MAXN]; // 记录前驱方格，用于回溯路径
long long nodeCnt = 0; // 出队的活结点个数

// 四个方向：上、下、左、右
const int dr[4] = { -1, 1, 0, 0 };
const int dc[4] = { 0, 0, -1, 1 };

bool InRange(int r, int c)
{
	return r >= 1 && r <= n && c >= 1 && c <= n;
}

// 队列式分支限界（本质上是按层次扩展的 BFS）
int ShortestPath()
{
	for (int i = 1; i <= n; ++i)
		for (int j = 1; j <= n; ++j)
			dist[i][j] = -1;
}

int main()
{
	cout << "请输入阵列规模 n：";
	cin >> n;
	cout << "请依次输入 " << n << " 行布线阵列（0 可布线，1 已封锁）：" << endl;
	for (int i = 1; i <= n; ++i)
		for (int j = 1; j <= n; ++j)
			cin >> grid[i][j];
	cout << "请输入布线起点 a（行 列）：";
	cin >> a.row >> a.col;
	cout << "请输入布线终点 b（行 列）：";
	cin >> b.row >> b.col;