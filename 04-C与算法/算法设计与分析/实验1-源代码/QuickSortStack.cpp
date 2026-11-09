// 快速排序的非递归实现 —— 用栈模拟递归
//
// 问题：对数组 23,45,17,11,13,89,72,26,3,17,11,13 用非递归算法排序。
//
// 思路：递归快排的本质是“先整体划分，再对左右两个子区间重复同样操作”。
// 需要保存的全部现场只有“子区间 (left, right)”这一对下标，
// 因此可以用一个显式栈保存待处理区间：循环取出区间做划分，
// 再把划分产生的两个子区间压栈，从而彻底消去函数递归调用。
//
// 与递归版本的对应关系：
//   递归调用 quicksort(l, q-1) / quicksort(q+1, r)  ==>  压栈
//   函数返回                                        ==>  出栈
//   递归深度                                        ==>  入栈时写入的 depth
//
// 一个小优化：每次先把较长的子区间压栈、较短的后压栈，
// 这样较短区间先被弹出处理，栈中最多同时保留 O(log n) 个区间，
// 最坏空间由 O(n) 降为 O(log n)，避免退化输入下的栈溢出。
//
// 编译：g++ -O2 -std=c++17 -static -o quick.exe QuickSortStack.cpp

#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

long long compareCnt = 0;          // 关键字比较次数统计

// ---------------------------------------------------------------
// 划分函数：挖坑法
// 取 a[p] 作基准（先把 a[p] 看成第一个“坑”），
// 右指针从右向左找小于基准的元素填到左坑，
// 左指针从左向右找大于基准的元素填到右坑，
// 两指针相遇处即为基准的最终位置。
// ---------------------------------------------------------------
int Partition(int a[], int p, int r) {
    int x = a[p];
    int i = p, j = r;
    while (i < j) {
        while (i < j && (++compareCnt, a[j] >= x)) --j;
        if (i < j) a[i++] = a[j];      // 填左坑，j 变成新坑
        while (i < j && (++compareCnt, a[i] <= x)) ++i;
        if (i < j) a[j--] = a[i];      // 填右坑，i 变成新坑
    }
    a[i] = x;                          // 基准归位
    return i;
}

void printArray(const int a[], int n, const string& tag) {
    cout << tag;
    for (int i = 0; i < n; ++i) {
        if (i) cout << ", ";
        cout << a[i];
    }
    cout << endl;
}

void printVals(int a[], int l, int r) {
    cout << "[";
    for (int i = l; i <= r; ++i) {
        if (i > l) cout << " ";
        cout << a[i];
    }
    cout << "]";
}

// 待处理区间；depth 记录它在递归树中的层数
struct Range { int left, right, depth; };

void pushRange(vector<Range>& stk, int l, int r, int d, bool shortOne) {
    stk.push_back({l, r, d});
    cout << "入栈：下标 [" << l << ", " << r << "]，深度 " << d;
    cout << (shortOne ? "（短区间）" : "（长区间）") << endl;
}

int main() {
    int data[] = {23, 45, 17, 11, 13, 89, 72, 26, 3, 17, 11, 13};
    int n = sizeof(data) / sizeof(data[0]);
    vector<int> a(data, data + n);

    cout << "===== 快速排序（非递归实现，用栈模拟递归）=====" << endl;
    printArray(a.data(), n, "初始数组：");
    cout << "元素个数 n = " << n << endl;

    vector<Range> stk;
    int maxStack = 0;

    stk.push_back({0, n - 1, 1});      // 初始区间 = 整个数组
    cout << "\n----- 初始状态 -----" << endl;
    cout << "入栈：区间下标 [0, " << n - 1 << "]，深度 1" << endl;

    int step = 0, pops = 0, maxDepth = 1;

    while (!stk.empty()) {
        Range cur = stk.back();
        stk.pop_back();                // 出栈 == “进入函数”
        ++pops;
        int l = cur.left, r = cur.right, d = cur.depth;
        if (d > maxDepth) maxDepth = d;

        cout << "\n----- 第 " << pops << " 次出栈 -----" << endl;
        cout << "区间下标 [" << l << ", " << r << "]，深度 " << d;
        cout << "，栈内剩余 " << stk.size() << " 个区间" << endl;
        cout << "区间内容：";
        printVals(a.data(), l, r);
        cout << endl;

        if (l >= r) {                  // 递归出口
            cout << "区间长度 " << (r - l + 1);
            cout << "，已达递归出口，直接返回" << endl;
            continue;
        }

        int pivot = a[l];
        int q = Partition(a.data(), l, r);
        ++step;
        cout << "以 " << pivot << " 为基准划分后：";
        printVals(a.data(), l, r);
        cout << endl;
        cout << "基准 " << pivot << " 归位到下标 " << q;
        cout << "，位置已最终确定" << endl;

        int l1 = l, r1 = q - 1;        // 左子区间
        int l2 = q + 1, r2 = r;        // 右子区间
        bool leftLonger = (r1 - l1) >= (r2 - l2);
        int d2 = d + 1;

        // 先压长区间、后压短区间 —— 短的先出栈被处理，栈深 O(log n)
        if (leftLonger) {
            if (l2 <= r2) pushRange(stk, l2, r2, d2, true);
            if (l1 <= r1) pushRange(stk, l1, r1, d2, false);
        } else {
            if (l1 <= r1) pushRange(stk, l1, r1, d2, true);
            if (l2 <= r2) pushRange(stk, l2, r2, d2, false);
        }
        if ((int)stk.size() > maxStack) maxStack = (int)stk.size();
        cout << "栈内待处理区间数 = " << stk.size() << endl;
    }

    cout << "\n===== 排序结果 =====" << endl;
    printArray(a.data(), n, "最终数组：");

    vector<int> ref(data, data + n);
    sort(ref.begin(), ref.end());
    cout << "\n===== 正确性校验 =====" << endl;
    cout << "与 std::sort 结果比对：";
    cout << (ref == a ? "完全一致，排序正确" : "不一致，存在错误") << endl;
    bool ordered = true;
    for (int i = 1; i < n; ++i) {
        if (a[i - 1] > a[i]) ordered = false;
    }
    cout << "非递减有序性检查：" << (ordered ? "通过" : "未通过") << endl;

    cout << "\n===== 统计信息 =====" << endl;
    cout << "出栈（= 递归调用）总次数 = " << pops << endl;
    cout << "实际划分次数 = " << step << "（每次划分确定 1 个位置）";
    cout << endl;
    cout << "关键字比较次数 = " << compareCnt << endl;
    cout << "最大递归深度（对应递归版） = " << maxDepth << " 层" << endl;
    cout << "栈的最大同时深度 = " << maxStack << " 个区间" << endl;
    cout << "平均 O(n log n)，最坏 O(n^2)，平均空间 O(log n)" << endl;
    return 0;
}
