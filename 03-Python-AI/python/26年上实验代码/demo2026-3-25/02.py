import numpy as np

num1=np.arange(8).reshape(2,4)
print(num1)
print(num1.ndim)
print(num1.shape)
print(num1.size)
print(num1.dtype)
print(num1.T)

#提取num1中的数字6
num2=num1[1][2]
print(num2)

num3=np.arange(12).reshape(3,4)
print(num3)
num4=num3[1:3]
print(num4)
num5=num3[:,1:3]
print(num5)
num6=num3[1:3,1:3]
print(num6)