/* shm.c -- 用共享存储区实现进程间通信
 * 编译: gcc shm.c -o shm
 * 运行: ./shm
 */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/wait.h>

#define SHMKEY 75          /* 共享存储区的键值 */
#define SHMSZ  1024        /* 共享区大小：1KB */

/* 约定：共享区第 1 个字节是"空标志"       */
/*   -1 : 共享区空闲，client 可以写入       */
/*   其它值 : 有数据，server 应当取走       */
/*   0  : 结束信号                          */

/* ---------- 服务进程：接收数据 ---------- */
void server(void)
{
    int shmid;
    signed char *addr;

    shmid = shmget(SHMKEY, SHMSZ, 0777 | IPC_CREAT);
    if (shmid == -1) {
        perror("server shmget");
        exit(1);
    }

    /* 附接到本进程的地址空间 */
    addr = (signed char *)shmat(shmid, NULL, 0);
    if (addr == (signed char *)-1) {
        perror("server shmat");
        exit(1);
    }

    addr[0] = -1;                       /* 置为空标志 */

    for (;;) {
        while (addr[0] == -1)           /* 忙等，直到 client 写入 */
            usleep(1000);

        printf("(server)received\n");

        if (addr[0] == 0) {             /* 0 为结束信号 */
            shmdt(addr);                /* 断开附接 */
            shmctl(shmid, IPC_RMID, 0); /* 撤销共享区 */
            exit(0);
        }
        addr[0] = -1;                   /* 处理完毕，恢复空闲 */
    }
}

/* ---------- 客户进程：发送数据 ---------- */
void client(void)
{
    int shmid, i;
    signed char *addr;

    shmid = shmget(SHMKEY, SHMSZ, 0777 | IPC_CREAT);
    if (shmid == -1) {
        perror("client shmget");
        exit(1);
    }

    addr = (signed char *)shmat(shmid, NULL, 0);
    if (addr == (signed char *)-1) {
        perror("client shmat");
        exit(1);
    }

    for (i = 9; i >= 0; i--) {
        while (addr[0] != -1)           /* 等 server 端空闲 */
            usleep(1000);

        addr[0] = (signed char)i;       /* 写入数据标志 */
        sprintf((char *)addr + 1, "message %d, length 1024 bytes", i);
        printf("(client)sent\n");
    }

    shmdt(addr);                        /* 断开附接后退出 */
    exit(0);
}

int main(void)
{
    pid_t pid1, pid2;

    if ((pid1 = fork()) == 0)           /* 第一个子进程作 server */
        server();

    if ((pid2 = fork()) == 0)           /* 第二个子进程作 client */
        client();

    waitpid(pid1, NULL, 0);             /* 父进程等两个子进程结束 */
    waitpid(pid2, NULL, 0);
    printf("(parent)exit\n");
    return 0;
}
