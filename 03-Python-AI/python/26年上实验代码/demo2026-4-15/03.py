import pandas as pd
from pandas import Series
from pandas import DataFrame
import numpy as np

data={
    '上海':[10,20,30]
    ,'北京':[40,50,60]
    ,'广州':[70,80,90]
}
df=DataFrame(data)
print(df)
list1=df.duplicated ()
print(list1)

print("==================")

data={'A':[10,20,30,10,20,30],'B':[40,50,60,40,50,60]}
print(df)
list2=df.duplicated()
print(list2)