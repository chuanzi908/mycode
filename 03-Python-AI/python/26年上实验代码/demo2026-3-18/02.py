#将一个整数列表中每个元素变为原来的2倍,定义1~20间的列表
if __name__ == '__main__':
    from random import randint
    list1 = [randint(1,20) for i in range(1,21)]
    list2 = [i*2 for i in list1]
    print(list2)
    print(list1)

