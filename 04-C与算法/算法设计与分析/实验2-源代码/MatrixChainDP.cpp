//
// 实验一：矩阵连乘问题 —— 动态规划（自底向上）
// 输入：矩阵个数 n，以及 n+1 个维度 p[0..n]
// 输出：最少连乘次数 m[1][n] 与最优计算次序
//
#include <iostream>
#include <iomanip>
#include <climits>
using namespace std;

const int MAXN = 50;
long long m[MAXN + 1][MAXN + 1];   // m[i][j]: A[i:j] 的最少连乘次数
int       s[MAXN + 1][MAXN + 1];   // s[i][j]: A[i:j] 的最优断开位置 k

int n;                             // 矩阵个数
int p[MAXN + 1];                   // 维度数组，A[i] 为 p[i-1] x p[i]

// 自底向上填表：先算长度 2 的子链，再算长度 3 …… 最后算长度 n
void matrixChain() {
    for (int i = 1; i <= n; ++i) m[i][i] = 0;          // 长度为 1 的链不需相乘
    for (int r = 2; r <= n; ++r) {                     // r 为链长
        for (int i = 1; i <= n - r + 1; ++i) {         // 链的起点
            int j = i + r - 1;                         // 链的终点
            m[i][j] = LLONG_MAX;
            for (int k = i; k < j; ++k) {              // 枚举断开位置
                long long t = m[i][k] + m[k + 1][j]
                            + (long long)p[i - 1] * p[k] * p[j];
                if (t < m[i][j]) {
                    m[i][j] = t;
                    s[i][j] = k;                       // 记录最优断开位置
                }
            }
        }
    }
}

// 由 s 表回溯构造最优计算次序
void traceback(int i, int j) {
    if (i == j) { cout << "A" << i; return; }
    cout << "(";
    traceback(i, s[i][j]);
    traceback(s[i][j] + 1, j);
    cout << ")";
}

int main() {
    cout << "输入矩阵数量n：";
    cin >> n;
    cout << "输入矩阵维度p0-p" << n << ": ";
    for (int i = 0; i <= n; ++i) cin >> p[i];

    matrixChain();

    cout << "\n===== 动态规划（自底向上）结果 =====\n";
    cout << "最少连乘次数 m[1][" << n << "] = " << m[1][n] << endl;
    cout << "最优计算次序: ";
    traceback(1, n);
    cout << endl;

    cout << "\n------ 断开位置表 s[i][j] ------\n";
    cout << " i\\j";
    for (int j = 1; j <= n; ++j) cout << setw(6) << j;
    cout << endl;
    for (int i = 1; i <= n; ++i) {
        cout << setw(4) << i;
        for (int j = 1; j <= n; ++j) {
            if (i <= j) cout << setw(6) << s[i][j];
            else        cout << setw(6) << "-";
        }
        cout << endl;
    }

    cout << "\n------ 最少连乘次数表 m[i][j] ------\n";
    cout << " i\\j";
    for (int j = 1; j <= n; ++j) cout << setw(9) << j;
    cout << endl;
    for (int i = 1; i <= n; ++i) {
        cout << setw(4) << i;
        for (int j = 1; j <= n; ++j) {
            if (i <= j) cout << setw(9) << m[i][j];
            else        cout << setw(9) << "-";
        }
        cout << endl;
    }
    return 0;
}
