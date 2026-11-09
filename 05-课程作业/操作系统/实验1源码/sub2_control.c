/* sub2_control.c  进程控制：每个进程输出一句话
 * 编译：gcc sub2_control.c -o sub2
 * 运行：./sub2
 */
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main(void)
{
    pid_t p1, p2;

    while ((p1 = fork()) == -1);

    if (p1 == 0) {                       /* 子进程 1 */
        printf("This is child process 1.\n");
        sleep(1);
    } else {
        while ((p2 = fork()) == -1);
        if (p2 == 0) {                   /* 子进程 2 */
            printf("This is child process 2.\n");
            sleep(2);
        } else {                         /* 父进程 */
            wait(NULL);                  /* 等待子进程结束，避免僵尸进程 */
            wait(NULL);
            printf("This is parent process.\n");
        }
    }
    return 0;
}
