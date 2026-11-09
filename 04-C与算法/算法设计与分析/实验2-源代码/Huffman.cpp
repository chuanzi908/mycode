//
// 实验三：哈夫曼编码 —— 贪心策略
// 输入：字符集与各字符出现的频率（权值）
// 输出：各字符的哈夫曼编码、加权路径长度 WPL、平均编码长度
//
#include <iostream>
#include <string>
#include <sstream>
#include <iomanip>
#include <cmath>
using namespace std;

const int MAXN = 100;
struct HTNode {
    double weight;          // 权值（频率）
    int    parent;          // 父结点下标，0 表示无父结点（根）
    int    lchild, rchild;  // 左、右孩子下标，0 表示无孩子
};
HTNode ht[2 * MAXN];        // 哈夫曼树：n 个叶结点 + (n-1) 个内部结点
string code[MAXN + 1];      // 各字符的哈夫曼编码
string ch[MAXN + 1];        // 各字符的名称
int n = 0;

// 在 1..m 中选出权值最小且没有父结点的两个结点，下标存入 s1、s2
void selectTwo(int m, int &s1, int &s2) {
    s1 = s2 = -1;
    for (int i = 1; i <= m; ++i) {
        if (ht[i].parent != 0) continue;                 // 已被合并，跳过
        if (s1 == -1 || ht[i].weight < ht[s1].weight) { s2 = s1; s1 = i; }
        else if (s2 == -1 || ht[i].weight < ht[s2].weight) { s2 = i; }
    }
}

// 构造哈夫曼树：每次贪心地合并权值最小的两棵子树
void createHuffmanTree() {
    int m = 2 * n - 1;                                   // 结点总数
    for (int i = 1; i <= m; ++i)
        ht[i].parent = ht[i].lchild = ht[i].rchild = 0;
    for (int i = n + 1; i <= m; ++i) {                    // 依次生成内部结点
        int s1, s2;
        selectTwo(i - 1, s1, s2);
        ht[s1].parent = ht[s2].parent = i;
        ht[i].lchild = s1;                                // 左孩子走 0
        ht[i].rchild = s2;                                // 右孩子走 1
        ht[i].weight = ht[s1].weight + ht[s2].weight;
    }
}

// 从叶结点向上回溯到根，得到各字符的哈夫曼编码
void buildCodes() {
    for (int i = 1; i <= n; ++i) {
        string c = "";
        int cur = i, fa = ht[cur].parent;
        while (fa != 0) {
            c = (ht[fa].lchild == cur ? "0" : "1") + c;
            cur = fa;
            fa = ht[cur].parent;
        }
        code[i] = c;
    }
}

int main() {
    string line;
    cout << "输入字符集：";
    getline(cin, line);
    istringstream iss(line);
    string token;
    while (iss >> token) ch[++n] = token;

    cout << "输入对应频率：";
    getline(cin, line);
    istringstream iss2(line);
    for (int i = 1; i <= n; ++i) iss2 >> ht[i].weight;

    createHuffmanTree();
    buildCodes();

    cout << "\n===== 哈夫曼编码结果 =====\n";
    cout << left << setw(10) << "字符" << setw(12) << "频率"
         << setw(18) << "哈夫曼编码" << "码长" << endl;
    cout << string(50, '-') << endl;

    double wpl = 0, totalFreq = 0;
    for (int i = 1; i <= n; ++i) {
        cout << setw(10) << ch[i]
             << setw(12) << ht[i].weight
             << setw(18) << code[i]
             << code[i].size() << endl;
        wpl       += ht[i].weight * code[i].size();
        totalFreq += ht[i].weight;
    }
    cout << string(50, '-') << endl;

    double avg = wpl / totalFreq;
    cout << fixed << setprecision(2);
    cout << "加权路径长度 WPL = " << wpl << endl;
    cout << "总频率           = " << totalFreq << endl;
    cout << "平均编码长度     = " << avg << " 位/字符" << endl;

    // 与等长编码比较：n 个字符至少需要 ceil(log2 n) 位
    int fixedLen = (int)ceil(log2((double)n));
    double fixedWpl = fixedLen * totalFreq;
    double rate = (fixedWpl - wpl) / fixedWpl * 100.0;
    cout << "\n等长编码（" << fixedLen << " 位）时：WPL = " << fixedWpl
         << "，平均长度 = " << fixedLen << " 位/字符" << endl;
    cout << "哈夫曼编码相对等长编码节省 " << rate << "% 的存储空间" << endl;
    return 0;
}
