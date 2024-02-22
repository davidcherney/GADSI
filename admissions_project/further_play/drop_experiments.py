import pandas as pd
import numpy as np

data = pd.DataFrame({'id':[3,5,2,6,1,3],'status':['s','f','s',  'u','s','u']})

df = data[ (data.status == 's') | (data.status == 'f')]
print(df)
# d= data.drop([2,6],axis=0)
# print(d)
# data.set_index('status')
# d = data.drop(index=['u'])
# print(d)
# group = data.groupby('status')
# ss = group.get_group('s')
# fs = group.get_group('f')
# clean = ss.join(fs)
# # print(data)
# print(clean)
# data = data.drop(['4'])
