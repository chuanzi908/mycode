import pandas as pdb
from pandas import Series
from pandas import DataFrame
import numpy as np

#创建一个二维数组
data=[[10,20,30],[40,50,60],[70,80,90]]
col=['平安','科技','幸福']
inde=['2000-3-1','2007-3-2','2012-3-3']
df=DataFrame(data,columns=col,index=inde)
print(df)
