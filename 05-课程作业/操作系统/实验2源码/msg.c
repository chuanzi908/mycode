/* msg.c -- 用消息队列实现进程间通信
 * 编译: gcc msg.c -o msg
 * 运行: ./msg
 */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <sys/wait.h>

#define MSGKEY 75          /* 消息队列的键值 */
#define MSGLEN 1024        /* 消息正文长度：1KB */

struct msgform {
    long mtype;            /* 消息类型，必须大于 0 */
    char mtext[MSGLEN];    /* 消息正文 */
} msg;

/* ---------- 服务进程：接收消息 ---------- */
void server(void)
{
    int qid;

    /* 建立（若不存在则创建）key 为 75 的消息队列 */
    qid = msgget(MSGKEY, 0777 | IPC_CREAT);
    if (qid == -1) {
        perror("server msgget");
        exit(1);
    }

    for (;;) {
        /* msgtyp = 0：接收队列中的第一个消息，不区分类型 */
        if (msgrcv(qid, &msg, MSGLEN, 0, 0) == -1) {
            perror("server msgrcv");
            exit(1);
        }
        printf("(server)received\n");

        /* 类型为 1 的消息是结束信号 */
        if (msg.mtype == 1) {
            msgctl(qid, IPC_RMID, 0);   /* 删除该消息队列 */
            exit(0);
        }
    }
}

/* ---------- 客户进程：发送消息 ---------- */
void client(void)
{
    int qid, i;

    /* 打开已存在的消息队列 */
    qid = msgget(MSGKEY, 0777);
    if (qid == -1) {
        perror("client msgget");
        exit(1);
    }

    for (i = 10; i >= 1; i--) {
        msg.mtype = i;                      /* 类型 10, 9, ..., 1 */
        sprintf(msg.mtext, "message %d", i);
        if (msgsnd(qid, &msg, MSGLEN, 0) == -1) {
            perror("client msgsnd");
            exit(1);
        }
        printf("(client)sent\n");
    }
    exit(0);
}

int main(void)
{
    pid_t pid1, pid2;

    if ((pid1 = fork()) == 0)       /* 第一个子进程作 server */
        server();

    if ((pid2 = fork()) == 0)       /* 第二个子进程作 client */
        client();

    waitpid(pid1, NULL, 0);         /* 父进程等两个子进程结束 */
    waitpid(pid2, NULL, 0);
    printf("(parent)exit\n");
    return 0;
}
