/* sub4_pipe.c  进程的管道通信
 * 编译：gcc sub4_pipe.c -o sub4
 * 运行：./sub4
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main(void)
{
    int fd[2];
    pid_t pid;
    char buf[128];

    if (pipe(fd) < 0) { perror("pipe"); exit(1); }   /* 创建管道 */
    if ((pid = fork()) < 0) { perror("fork"); exit(1); }

    if (pid == 0) {                    /* 子进程：读管道 */
        close(fd[1]);                  /* 关闭不用的写端 */
        memset(buf, 0, sizeof(buf));
        read(fd[0], buf, sizeof(buf) - 1);   /* 无数据时阻塞等待 */
        printf("child process received: %s\n", buf);
        close(fd[0]);
        exit(0);
    } else {                           /* 父进程：写管道 */
        const char *msg = "Hello, I am your parent process!";
        close(fd[0]);                  /* 关闭不用的读端 */
        write(fd[1], msg, strlen(msg));
        printf("parent process sent: %s\n", msg);
        close(fd[1]);                  /* 写完关闭，读端才会读到 EOF */
        wait(NULL);
        printf("parent process is killed!\n");
    }
    return 0;
}
