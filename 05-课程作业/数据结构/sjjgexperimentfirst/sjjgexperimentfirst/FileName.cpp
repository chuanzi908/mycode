#include <stdio.h>
#include <stdlib.h>

typedef struct BSTNode {
    int key;
    struct BSTNode* lchild, * rchild;
} BSTNode, * BSTree;

// 插入结点
void InsertBST(BSTree* T, int key) {
    if (!*T) {
        *T = (BSTree)malloc(sizeof(BSTNode));
        (*T)->key = key;
        (*T)->lchild = (*T)->rchild = NULL;
    }
    else if (key < (*T)->key) InsertBST(&(*T)->lchild, key);
    else InsertBST(&(*T)->rchild, key);
}

// 删除结点
void Delete(BSTree* p) {
    BSTree q, s;
    if (!(*p)->lchild) { // 无左孩子
        q = *p; *p = (*p)->rchild; free(q);
    }
    else if (!(*p)->rchild) { // 无右孩子
        q = *p; *p = (*p)->lchild; free(q);
    }
    else { // 左右孩子都有
        q = *p; s = (*p)->lchild;
        while (s->rchild) { q = s; s = s->rchild; }
        (*p)->key = s->key;
        if (q != *p) q->rchild = s->lchild;
        else q->lchild = s->lchild;
        free(s);
    }
}

// 查找并删除
int DeleteBST(BSTree* T, int key) {
    if (!*T) return 0;
    else {
        if (key == (*T)->key) { Delete(T); return 1; }
        else if (key < (*T)->key) return DeleteBST(&(*T)->lchild, key);
        else return DeleteBST(&(*T)->rchild, key);
    }
}

// 中序遍历
void InOrder(BSTree T) {
    if (T) {
        InOrder(T->lchild);
        printf("%d ", T->key);
        InOrder(T->rchild);
    }
}

int main() {
    BSTree T = NULL;
    int key, opt;
    while (1) {
        printf("1-插入 2-删除 0-退出：");
        scanf("%d", &opt);
        if (opt == 0) break;
        else if (opt == 1) {
            printf("输入插入值：");
            scanf("%d", &key);
            InsertBST(&T, key);
        }
        else if (opt == 2) {
            printf("输入删除值：");
            scanf("%d", &key);
            DeleteBST(&T, key);
        }
        printf("中序序列："); InOrder(T); printf("\n");
    }
    return 0;
}