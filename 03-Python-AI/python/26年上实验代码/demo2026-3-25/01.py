import numpy as np

# 创建一维数组，包含 5 个元素 [1,2,3,4,5]
num1=np.array([1,2,3,4,5])
print(num1)

# 创建二维数组（矩阵），2 行 3 列 [[1,2,3],[4,5,6]]
num2=np.array([[1,2,3],[4,5,6]])
print(num2)

# 创建等差数列，从 0 到 10（不包含 10），步长为 2，结果 [0,2,4,6,8]
num3=np.arange(0,10,2)
print(num3)

# 创建 0 到 11 的数组，重塑为 3 行 4 列的二维数组
num4=np.arange(12).reshape(3,4)
print(num4)


# 创建随机整数数组，生成 3 个 1 到 10（不包含 10）之间的随机整数
num5=np.random.randint(1,10,size=(3))
print(num5)

# 创建随机小数数组，生成 3 行 4 列的二维数组，元素为 0 到 1 之间的随机小数
num6=np.random.rand(3,4)
print(num6)