import numpy as np

# 创建随机整数数组，生成 12 个 1 到 50（不包含 50）的随机整数，重塑为 3 行 4 列的二维数组
num1=np.random.randint(1,50,size=12).reshape(3,4)
print(num1)

# 对数组进行排序，axis=0 表示按列排序（纵向排序）
num1.sort(axis=0)
print(num1)