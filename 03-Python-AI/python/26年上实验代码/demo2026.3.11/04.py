#定义一个人员基本信息列表然后通过列表信息结合控制台将值录入,生成字典信息,并进行输出打印
if __name__ == '__main__':
    person_info = ['姓名', '性别', '年龄', '电话']
    person_info_dict = dict(zip(person_info, input("请输入人员信息：").split()))
    print(person_info_dict)

