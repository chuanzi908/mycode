#通过控制台，接收输入的10个整数，并将输入的内容放到集合当中，
#  利用循环计算此集合当中的数的总。最终输出集合及总数
if __name__ == '__main__':
    # 初始化空集合
    num_set = set()

    # 循环接收10个整数输入
    for i in range(10):
        while True:
            # 提示用户输入，并显示当前是第几次输入
            input_str = input(f"请输入第{i + 1}个整数：")
            try:
                # 将输入转换为整数
                num = int(input_str)
                # 将整数添加到集合中
                num_set.add(num)
                break  # 输入正确则退出内层循环，继续下一次输入
            except ValueError:
                # 输入不是整数时提示错误
                print("输入错误，请输入有效的整数！")

    # 计算集合中所有元素的总和
    total = sum(num_set)

    # 输出结果
    print("\n最终的集合：", num_set)
    print("集合中元素的总和：", total)