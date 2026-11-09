import pandas as pdb
from pandas import Series
from pandas import DataFrame
import numpy as np

listnum=Series([11,21,31,41,51])
#print(listnum)

chengji=Series(np.array((90,85,70)),index=['语文','英语','数学'])
print(chengji)

#通过控制台输入5个值,此值为银行每天收入,通过索引将输入的值与之匹配,并将各个银行的收入进行输出
# ... existing code ...

bank_names = ['银行 A', '银行 B', '银行 C', '银行 D', '银行 E']
bank_incomes = []

for i in range(5):
    num = int(input('请输入第%d天的收入:' % (i + 1)))
    bank_incomes.append(num)
    print('第%d天的收入是:%d' % (i + 1, num))

bank = Series(np.array(bank_incomes), index=bank_names)
print('\n各个银行的收入:')
print(bank)



#在上述实例中,对五个银行的信息进行截取3家银行并输出.
#同时对三家当中第2家的数值进行修改,改为20000
#删除第三家公司
#最终增加一个新银行公司,输出最终结果

# 1. 截取前 3 家银行
bank_slice = bank.iloc[:3]
print('\n截取前 3 家银行:')
print(bank_slice)

# 2. 修改第 2 家银行的数值为 20000
bank_slice.iloc[1] = 20000
print('\n修改第 2 家银行收入为 20000:')
print(bank_slice)

# 3. 删除第三家公司
bank_slice = bank_slice.drop(bank_slice.index[2])
print('\n删除第三家公司后:')
print(bank_slice)

# 4. 增加一个新银行公司
new_bank = Series([50000], index=['银行 F'])
bank_final = pdb.concat([bank_slice, new_bank])
print('\n增加新银行后的最终结果:')
print(bank_final)


