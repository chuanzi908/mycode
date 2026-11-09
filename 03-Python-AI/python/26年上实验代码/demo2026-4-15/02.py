import pandas as pd
from pandas import Series
from pandas import DataFrame

data=[[10,20,30],[40,50,60],[70,80,90]]

df=DataFrame(data,index=['一月','二月','三月'],columns=['美团','京东','淘宝'])

print(df)
list=df.astype(float)
print(list)