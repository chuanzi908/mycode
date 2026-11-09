#通过函数编写一个9x9乘法表,参数用来控制乘法表输出的个数,默认输出9x9
def multiplication_table(n=9):
    """
    打印 n x n 乘法表

    参数:
        n: 控制乘法表的大小，默认为 9
    """
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            print(f"{j}×{i}={i * j}", end="\t")
        print()


# 测试函数
if __name__ == "__main__":
    print("9x9 乘法表:")
    multiplication_table()



