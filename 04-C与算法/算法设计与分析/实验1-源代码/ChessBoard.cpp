// 棋盘覆盖问题 —— 分治算法（L 型骨牌覆盖）
//
// 问题：在 2^k × 2^k 的棋盘中恰有一个特殊方格，用 4 种形态的
// L 型骨牌覆盖除特殊方格外的全部方格，任意两块骨牌不得重叠。
//
// 分治策略：
//   把棋盘等分为 4 个 2^(k-1) × 2^(k-1) 的子棋盘，特殊方格必居其一；
//   在中心交界处放一块 L 型骨牌，恰好盖住其余 3 个子棋盘各自的角格，
//   于是 4 个子棋盘都变成“各含一个特殊方格”的同类子问题，递归求解。
//
// 递归方程：T(1) = O(1)，T(2^k) = 4 T(2^(k-1)) + O(1)
// 由主定理（a = 4, b = 2, log_b a = 2 > 0）得 T(n) = O(n^2)。
// 骨牌总数为 (4^k - 1)/3，与棋盘格数同阶，故该算法已达最优。
//
// 编译：g++ -O2 -std=c++17 -static -o chess.exe ChessBoard.cpp

#include <iostream>
#include <iomanip>
using namespace std;

const int MAXN = 130;              // 支持 2^7 = 128 及以内的棋盘

int board[MAXN][MAXN];             // 骨牌编号，0 表示特殊方格
int tile = 0;                      // 骨牌编号计数器，全局递增保证不重复
int n;                             // 棋盘边长 2^k

long long recurCalls = 0;           // 递归调用次数
int maxDepth = 0;                   // 实际递归深度

// ---------------------------------------------------------------
// 分治主体
//   tr, tc : 当前子棋盘左上角坐标
//   dr, dc : 特殊方格坐标
//   size   : 当前子棋盘边长
// ---------------------------------------------------------------
void chessBoard(int tr, int tc, int dr, int dc, int size, int depth) {
    ++recurCalls;
    if (depth > maxDepth) maxDepth = depth;

    if (size == 1) return;         // 递归出口：只剩 1 格且必为特殊格

    int s = size / 2;              // 二分子棋盘
    int t = ++tile;                // 本层使用一块新骨牌，编号 t

    // 左上子棋盘：特殊方格在其中
    if (dr < tr + s && dc < tc + s) {
        chessBoard(tr, tc, dr, dc, s, depth + 1);
    } else {
        board[tr + s - 1][tc + s - 1] = t;      // 左上子棋盘的右下角
        chessBoard(tr, tc, tr + s - 1, tc + s - 1, s, depth + 1);
    }

    // 右上子棋盘
    if (dr < tr + s && dc >= tc + s) {
        chessBoard(tr, tc + s, dr, dc, s, depth + 1);
    } else {
        board[tr + s - 1][tc + s] = t;          // 右上子棋盘的左下角
        chessBoard(tr, tc + s, tr + s - 1, tc + s, s, depth + 1);
    }

    // 左下子棋盘
    if (dr >= tr + s && dc < tc + s) {
        chessBoard(tr + s, tc, dr, dc, s, depth + 1);
    } else {
        board[tr + s][tc + s - 1] = t;          // 左下子棋盘的右上角
        chessBoard(tr + s, tc, tr + s, tc + s - 1, s, depth + 1);
    }

    // 右下子棋盘
    if (dr >= tr + s && dc >= tc + s) {
        chessBoard(tr + s, tc + s, dr, dc, s, depth + 1);
    } else {
        board[tr + s][tc + s] = t;              // 右下子棋盘的左上角
        chessBoard(tr + s, tc + s, tr + s, tc + s, s, depth + 1);
    }
}

// 打印棋盘：每格占 4 字符宽
void printBoard(int size) {
    for (int i = 1; i <= size; ++i) {
        if (i == 1) {
            for (int j = 1; j <= size; ++j) cout << "----";
            cout << "\n";
        }
        for (int j = 1; j <= size; ++j) cout << setw(4) << board[i][j];
        cout << "\n";
    }
}

int main() {
    int k, sr, sc;
    cout << "请输入棋盘规模 k（棋盘为 2^k × 2^k）：";
    cin >> k;
    cout << "请输入特殊方格坐标（行 列，1-based）：";
    cin >> sr >> sc;

    n = 1 << k;
    if (k < 0 || k > 7 || sr < 1 || sr > n || sc < 1 || sc > n) {
        cout << "输入非法：k 应在 [0,7]，坐标应在 [1," << n << "] 内。";
        cout << endl;
        return 1;
    }

    for (int i = 1; i <= n; ++i)
        for (int j = 1; j <= n; ++j)
            board[i][j] = 0;
    tile = 0; recurCalls = 0; maxDepth = 0;

    board[sr][sc] = 0;                       // 特殊方格标记为 0
    chessBoard(1, 1, sr, sc, n, 1);          // 从整块棋盘开始分治

    cout << "\n===== 棋盘覆盖结果（0 为特殊方格，数字为骨牌编号）";
    cout << "=====" << endl;
    if (n <= 16) {
        printBoard(n);
    } else {
        for (int i = 1; i <= 8; ++i) {
            for (int j = 1; j <= 8; ++j) cout << setw(4) << board[i][j];
            cout << "  ...\n";
        }
        cout << "（棋盘过大，仅显示左上 8×8）" << endl;
    }

    cout << "\n===== 统计信息 =====" << endl;
    cout << "棋盘规模 n = " << n << " × " << n << endl;
    cout << "使用的 L 型骨牌块数 = " << tile << "（理论值 (4^k - 1)/3";
    cout << " = " << ((long long)n * n - 1) / 3 << "）" << endl;
    cout << "递归调用总次数 = " << recurCalls << endl;
    cout << "最大递归深度 = " << maxDepth << endl;
    cout << "时间复杂度 O(n^2) = " << (long long)n * n << " 量级" << endl;
    return 0;
}
