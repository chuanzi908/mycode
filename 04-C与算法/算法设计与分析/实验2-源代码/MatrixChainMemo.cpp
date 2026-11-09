//
// 实验二：矩阵连乘问题 —— 备忘录方法（自顶向下）
// 与动态规划结果一致，但计算顺序是"需要时才递归求解"，
// 求解前先查表，若已算过则直接返回，避免重复计算。
//
#include <iostream>
#include <iomanip>
#include <climits>
using namespace std;

const int MAXN = 50;
long long m[MAXN + 1][MAXN + 1];   // 备忘录，0 表示"尚未计算"
int       s[MAXN + 1][MAXN + 1];
int       n;
int       p[MAXN + 1];

long long lookUpChainCnt = 0;      // 查表次数（统计用）
long long computeCnt     = 0;      // 实际求解的子问题个数（统计用）

long long lookupChain(int i, int j) {
    if (m[i][j] > 0) { ++lookUpChainCnt; return m[i][j]; }  // 查表命中
    if (i == j) { m[i][j] = 0; return 0; }                  // 递归边界

    ++computeCnt;                                           // 真正做了一次计算
    m[i][j] = LLONG_MAX;
    for (int k = i; k < j; ++k) {
        long long t = lookupChain(i, k) + lookupChain(k + 1, j)
                    + (long long)p[i - 1] * p[k] * p[j];
        if (t < m[i][j]) {
            m[i][j] = t;
            s[i][j] = k;
        }
    }
    return m[i][j];
}

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

    for (int i = 1; i <= n; ++i)
        for (int j = 1; j <= n; ++j) m[i][j] = 0;   // 备忘录初始化

    long long best = lookupChain(1, n);

    cout << "\n===== 备忘录方法（自顶向下）结果 =====\n";
    cout << "最少连乘次数 m[1][" << n << "] = " << best << endl;
    cout << "最优计算次序: ";
    traceback(1, n);
    cout << endl;

    cout << "\n统计信息：\n";
    cout << "  实际求解子问题个数 = " << computeCnt << endl;
    cout << "  其中的子问题规模数 = " << n * (n + 1) / 2
         << "（i<=j 的组合数，即与动态规划同量级）" << endl;
    cout << "  查表命中次数       = " << lookUpChainCnt << endl;

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
    return 0;
}
