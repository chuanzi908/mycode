#定义图书信息结构,并将5本信息入库,最后将库中的信息进行显示
if __name__ == '__main__':
    str1 = ('编号', '书名', '作者', '出版社', '价格')
    dict1={}
    for i in range(5):
        dict1[i+1]=input("请输入图书信息：").split()
    print(dict1)