/* sub1_create.c  进程的创建
 * 编译：gcc sub1_create.c -o sub1
 * 运行：./sub1
 */
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>

int main(void)
{
    pid_t p1, p2;

    while ((p1 = fork()) == -1);        /* 创建子进程 p1 */

    if (p1 == 0) {                      /* 子进程 p1 */
        putchar('b');
    } else {                            /* 父进程 */
        while ((p2 = fork()) == -1);    /* 创建子进程 p2 */
        if (p2 == 0) {                  /* 子进程 p2 */
            putchar('c');
        } else {                        /* 仍是父进程 */
            putchar('a');
        }
    }
    return 0;
}
