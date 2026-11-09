#include <iostream>
#include <cstring>
using namespace std;

// ===================== 1. 矩阵鞍点 =====================
void FindSaddlePoint(int a[][3], int n) {
    cout << "===== 矩阵鞍点查找 =====" << endl;
    for (int i = 0; i < n; i++) {
        // 找第i行最大值
        int maxVal = a[i][0];
        int col = 0;
        for (int j = 1; j < n; j++) {
            if (a[i][j] > maxVal) {
                maxVal = a[i][j];
                col = j;
            }
        }
        // 判断是否为该列最小
        bool ok = true;
        for (int k = 0; k < n; k++) {
            if (a[k][col] < maxVal) {
                ok = false;
                break;
            }
        }
        if (ok) {
            cout << "鞍点：a[" << i << "][" << col << "] = " << maxVal << endl;
            return;
        }
    }
    cout << "无鞍点" << endl;
}

// ===================== 2. 约瑟夫环（循环链表） =====================
struct Node {
    int id;
    Node* next;
    Node(int x) : id(x), next(NULL) {}
};

void Josephus(int n, int m) {
    cout << "\n===== Josephus问题 n=" << n << " m=" << m << " =====" << endl;
    if (n <= 0 || m <= 0) return;

    Node* head = new Node(1);
    Node* tail = head;
    for (int i = 2; i <= n; i++) {
        tail->next = new Node(i);
        tail = tail->next;
    }
    tail->next = head;

    Node* cur = head;
    Node* pre = tail;
    int cnt = 1;

    cout << "出列顺序：";
    while (cur->next != cur) {
        if (cnt == m) {
            cout << cur->id << " ";
            pre->next = cur->next;
            delete cur;
            cur = pre->next;
            cnt = 1;
        }
        else {
            pre = cur;
            cur = cur->next;
            cnt++;
        }
    }
    cout << "\n最后一人：" << cur->id << endl;
    delete cur;
}

// ===================== 3. 停车场模拟（栈+队列） =====================
const int MAX_CAR = 3;

struct Car {
    int id;
    int time;
};

// 停车场栈
class Stack {
private:
    Car data[MAX_CAR];
    int top;
public:
    Stack() : top(-1) {}
    bool Push(Car c) {
        if (top >= MAX_CAR - 1) return false;
        data[++top] = c;
        return true;
    }
    Car Pop() { return data[top--]; }
    bool IsFull() { return top == MAX_CAR - 1; }
    bool IsEmpty() { return top == -1; }
    int Find(int id) {
        for (int i = 0; i <= top; i++)
            if (data[i].id == id) return i;
        return -1;
    }
    Car Get(int pos) { return data[pos]; }
    void Remove(int pos) {
        for (int i = pos; i < top; i++)
            data[i] = data[i + 1];
        top--;
    }
    void Show() {
        for (int i = 0; i <= top; i++)
            cout << data[i].id << " ";
    }
};

// 便道队列
class Queue {
private:
    Car data[100];
    int front, rear;
public:
    Queue() : front(0), rear(0) {}
    void EnQueue(Car c) { data[rear++] = c; }
    Car DeQueue() { return data[front++]; }
    bool IsEmpty() { return front == rear; }
};

void ParkingSim() {
    cout << "\n===== 停车场模拟 =====" << endl;
    Stack park;
    Queue wait;
    char op;
    int id, t;

    while (1) {
        cin >> op >> id >> t;
        if (op == 'E') break;

        if (op == 'A') {
            Car c = { id, t };
            if (!park.IsFull()) park.Push(c);
            else wait.EnQueue(c);
        }
        else if (op == 'D') {
            int pos = park.Find(id);
            if (pos == -1) continue;
            Car outCar = park.Get(pos);
            cout << "车辆" << id << "离开，停留时长：" << t - outCar.time << endl;
            park.Remove(pos);

            if (!wait.IsEmpty()) {
                Car c = wait.DeQueue();
                c.time = t;
                park.Push(c);
            }
        }
        cout << "停车场车辆："; park.Show(); cout << endl;
    }
}

// ===================== 主函数 =====================
int main() {
    // 1. 鞍点测试
    int mat[3][3] = { 1,2,3,4,5,6,7,8,9 };
    FindSaddlePoint(mat, 3);

    // 2. 约瑟夫环测试
    Josephus(8, 3);
    Josephus(100, 5);

    // 3. 停车场模拟
    ParkingSim();

    return 0;
}