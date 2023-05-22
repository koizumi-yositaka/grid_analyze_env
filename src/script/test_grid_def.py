
'''
from src import analyze_grid_def
import pytest

ag=analyze_grid_def.AnalyzeGrid("test/gridByItems/part1.txt")
ag.analyze() 
ag.write("test/gridByItems")

import tool
str_test="ボタンテキスト~#U#RL~=フォー=ム項目リストの書式"
delimiter="#@~="
ary=[]
result_ary=[]
del_ary=delimiter.split("@")
for i in range(len(del_ary)):
    del_ary[i]=tool.get_delimiter(str_test,del_ary[i])
    index=str_test.find(del_ary[i])
    if index < 0:
        pass
    else:
        ary.append(index)
print(ary)
index=0
for i in range(len(ary)):
    if ary[i]<0: continue
    result_ary.append(str_test[index:ary[i]])
    index=ary[i]+len(del_ary[i])
result_ary.append(str_test[index:])
print(result_ary)'''