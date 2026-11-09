import pandas as pd
from pandas import Series
from pandas import DataFrame
import numpy as np

#普通序列
data1=pd.Series([1,2,3,4,5,6,7,8,9,10])
#转换为浮点
data=data1.astype(float)
print(data)

Q1=data.quantile(0.25)
Q3=data.quantile(0.75)

lower=Q1-1.5*(Q3-Q1)
upper=Q3+1.5*(Q3-Q1)

outlnes=(data<lower)|(data>upper)
#计算均值
mearn_value=data[~outlnes].mean()