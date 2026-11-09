/* sub3_signal.c  进程的软中断通信
 * 编译：gcc sub3_signal.c -o sub3
 * 运行：./sub3
 *
 * 对比实验：把下面两行 signal(SIGINT/SIGQUIT, SIG_IGN) 注释掉后重新编译运行，
 *           再在程序等待期间按 Ctrl+C，观察父、子进程的不同命运。
 */
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int wait_mark = 0;      /* 子进程的同步标志 */
int ack = 0;            /* 父进程已收到的应答数 */

void stop(int signo)            /* 子进程用：收到软中断后解除挂起 */
{
    wait_mark = 0;
}

void child_ack(int signo)       /* 父进程用：统计子进程的应答 */
{
    ack++;
}

int main(void)
{
    pid_t p1, p2;

    /* 【关键语句】父进程忽略键盘中断，使 Ctrl+C / Ctrl+\ 只作用于子进程 */
    signal(SIGINT,  SIG_IGN);
    signal(SIGQUIT, SIG_IGN);

    if ((p1 = fork()) == 0) {           /* 子进程 1 */
        wait_mark = 1;
        signal(SIGUSR1, stop);          /* 注册软中断处理函数 */
        while (wait_mark) pause();      /* 挂起，等待父进程的软中断 */
        printf("child process 1 is killed by parent!\n");
        kill(getppid(), SIGUSR2);       /* 向父进程应答 */
        exit(0);
    }

    if ((p2 = fork()) == 0) {           /* 子进程 2 */
        wait_mark = 1;
        signal(SIGUSR2, stop);
        while (wait_mark) pause();
        printf("child process 2 is killed by parent!\n");
        kill(getppid(), SIGUSR2);
        exit(0);
    }

    /* ===== 父进程 ===== */
    signal(SIGUSR2, child_ack);         /* 注册“子进程应答”处理函数 */
    sleep(3);                           /* 先让两个子进程进入等待 */
    printf("parent: send soft interrupt to children\n");
    kill(p1, SIGUSR1);                  /* 向子进程 1 发软中断 */
    kill(p2, SIGUSR2);                  /* 向子进程 2 发软中断 */

    while (ack < 2) pause();            /* 等待两个子进程应答 */
    wait(NULL);
    wait(NULL);
    printf("parent process is killed!\n");
    return 0;
}
