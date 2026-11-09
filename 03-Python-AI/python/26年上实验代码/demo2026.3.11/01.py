if __name__ == '__main__':
    #模版
    str="姓名:{}\n性别:{}\n学号:{}"
    #接收控制台输入的信息
    num1=input("请输入姓名：")
    num2=input("请输入性别：")
    num3=input("请输入学号：")
    #输出结果
    print(str.format(num1,num2,num3))