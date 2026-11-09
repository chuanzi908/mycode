import pandas as pd
from pandas import Series
import numpy as np

# 创建第一个序列 - 银行 A 的收入数据
bank_a = Series([10000, 15000, 12000, 18000, 20000],
                index=['周一', '周二', '周三', '周四', '周五'],
                name='银行 A')

# 创建第二个序列 - 银行 B 的收入数据
bank_b = Series([8000, 11000, 9500, 14000, 16000],
                index=['周一', '周二', '周三', '周四', '周五'],
                name='银行 B')

print('银行 A 的收入:')
print(bank_a)
print('\n银行 B 的收入:')
print(bank_b)

# 合并两个序列（使用 concat）
combined = pd.concat([bank_a, bank_b])
print('\n合并后的序列:')
print(combined)

# 或者按列合并成 DataFrame
df = pd.DataFrame({'银行 A': bank_a, '银行 B': bank_b})
print('\n按列合并成 DataFrame:')
print(df)
