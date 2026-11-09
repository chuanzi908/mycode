#include <stdio.h>
#include <stdlib.h>
#define MAXSIZE 100

// 二叉链表结点结构
typedef struct BiTNode {
    char data;
    struct BiTNode* lchild, * rchild;
} BiTNode, * BiTree;

// 循环队列结构
typedef struct {
    BiTree data[MAXSIZE];
    int front, rear;
} Queue;

// 初始化队列
void InitQueue(Queue* Q) {
    Q->front = Q->rear = 0;
}

// 入队
int EnQueue(Queue* Q, BiTree T) {
    if ((Q->rear + 1) % MAXSIZE == Q->front) return 0;
    Q->data[Q->rear] = T;
    Q->rear = (Q->rear + 1) % MAXSIZE;
    return 1;
}

// 出队
int DeQueue(Queue* Q, BiTree* T) {
    if (Q->front == Q->rear) return 0;
    *T = Q->data[Q->front];
    Q->front = (Q->front + 1) % MAXSIZE;
    return 1;
}

// 按层次创建二叉树
void CreateBiTree(BiTree* T) {
    char ch;
    Queue Q;
    InitQueue(&Q);
    *T = NULL;
    printf("请输入结点值（*为空，#结束）：");
    scanf(" %c", &ch);
    if (ch != '#') {
        *T = (BiTree)malloc(sizeof(BiTNode));
        (*T)->data = ch;
        (*T)->lchild = (*T)->rchild = NULL;
        EnQueue(&Q, *T);
    }
    while (Q.front != Q.rear) {
        BiTree p;
        DeQueue(&Q, &p);
        // 左孩子
        printf("请输入%c的左孩子（*为空，#结束）：", p->data);
        scanf(" %c", &ch);
        if (ch == '#') break;
        if (ch != '*') {
            p->lchild = (BiTree)malloc(sizeof(BiTNode));
            p->lchild->data = ch;
            p->lchild->lchild = p->lchild->rchild = NULL;
            EnQueue(&Q, p->lchild);
        }
        else p->lchild = NULL;
        // 右孩子
        printf("请输入%c的右孩子（*为空，#结束）：", p->data);
        scanf(" %c", &ch);
        if (ch == '#') break;
        if (ch != '*') {
            p->rchild = (BiTree)malloc(sizeof(BiTNode));
            p->rchild->data = ch;
            p->rchild->lchild = p->rchild->rchild = NULL;
            EnQueue(&Q, p->rchild);
        }
        else p->rchild = NULL;
    }
}

// 层次遍历
void LevelOrder(BiTree T) {
    if (!T) return;
    Queue Q;
    InitQueue(&Q);
    EnQueue(&Q, T);
    printf("层次遍历序列：");
    while (Q.front != Q.rear) {
        BiTree p;
        DeQueue(&Q, &p);
        printf("%c ", p->data);
        if (p->lchild) EnQueue(&Q, p->lchild);
        if (p->rchild) EnQueue(&Q, p->rchild);
    }
    printf("\n");
}

int main() {
    BiTree T;
    CreateBiTree(&T);
    LevelOrder(T);
    return 0;
}