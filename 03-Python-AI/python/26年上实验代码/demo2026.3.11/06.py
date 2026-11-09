#通过获取年龄,判断是否成年
if __name__ == '__main__':
    age = input("请输入年龄：")
    if int(age) >= 18:
        print("已成年")
    else:
        print("未成年")