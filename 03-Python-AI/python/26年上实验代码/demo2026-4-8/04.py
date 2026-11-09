import pandas as pd
from pandas import Series
from pandas import DataFrame

# 学号完全相同的情况下合并
intList1 = pd.DataFrame({'学号':['201','202','203'],'语文':[10,20,30],'数学':[20,30,40]})
intList2 = pd.DataFrame({'学号':['202','201','203'],'英语':[10,20,30],'历史':[20,30,40]})
List3 = pd.merge(intList1,intList2,on='学号')

# 要合并的学号与合并学号存在差异的情况下，使用how参数进行指定
intList3 = pd.DataFrame({'学号':['201','202','204'],'地理':[10,20,30],'生物':[20,30,40]})

# 内连接（默认inner） how （inner , left, right, outer）
List3 = pd.merge(intList1,intList3,on='学号',how='outer')
print(List3)