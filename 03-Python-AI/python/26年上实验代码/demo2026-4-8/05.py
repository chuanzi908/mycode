import numpy as np
from pandas import DataFrame

# 1. 创建包含缺失值(NaN)的元数据
list1 = np.array([
    [163, 113, 158],
    [np.nan, np.nan, 119],
    [193, 127, np.nan],
    [109, 126, 110]
])

# 构建DataFrame，指定行索引和列名
df = DataFrame(
    list1,
    index=['一月', '二月', '三月', '四月'],
    columns=['美好集团', '上海集团', '深圳集团']
)
print("=== 原始数据（含缺失值） ===")
print(df)
print("\n")

# 2. 检测缺失值：isna() 与 isnull() 效果完全一致
list2 = df.isna()
print("=== df.isna() 检测缺失值（True为缺失）===")
print(list2)
print("\n")

list3 = df.isnull()
print("=== df.isnull() 检测缺失值（与isna()等价）===")
print(list3)
print("\n")

# 3. 删除缺失值的行数据
list4 = df.dropna()
print("=== 删除含缺失值的行后 ===")
print(list4)
print("\n")

# 4. 填充缺失值为0
list5 = df.fillna(0)
print("=== 缺失值填充为0后 ===")
print(list5)
print("\n")

# 5. 向上填充（用下一行数据填补上一行的缺失值）
list6 = df.bfill()
print("=== 向上填充（bfill）后 ===")
print(list6)
print("\n")

# 6. 向下填充（用上一行数据填补下一行的缺失值）
list7 = df.ffill()
print("=== 向下填充（ffill）后 ===")
print(list7)