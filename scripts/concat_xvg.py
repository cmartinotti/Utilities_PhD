#!/usr/bin/env python
#THIS SCRIPT IS CALLED LIKE:
# concat_xvg.py file1.xvg file2.xvg outputname
#it will just merge them together reindexing the time assuming it has a timestep of 2 ps

import numpy as np
import pandas as pd
import re
import sys

with open (sys.argv[1],'r') as f:
    read_data=f.read()
f.close
temp_list=read_data.split('\n')

titles=[]
tempvalues=[]
for i in range(len(temp_list)-1):
   if "@" in temp_list[i] or "#" in temp_list[i]:
        if re.search("xaxis",temp_list[i]):
            titles.append(" ".join(temp_list[i].split()[3:]).strip('"'))
        elif re.search("s[0-9] legend",temp_list[i]):
            titles.append(" ".join(temp_list[i].split()[3:]).strip('"'))
        else:
            continue
   else:
      tempvalues.append(temp_list[i].split())
values=np.array(tempvalues)
values=values.astype(float)

with open (sys.argv[2],'r') as f2:
    read_data=f2.read()
f2.close
temp_list=read_data.split('\n')

titles=[]
tempvalues2=[]
for i in range(len(temp_list)-1):
   if "@" in temp_list[i] or "#" in temp_list[i]:
        if re.search("xaxis",temp_list[i]):
            titles.append(" ".join(temp_list[i].split()[3:]).strip('"'))
        elif re.search("s[0-9] legend",temp_list[i]):
            titles.append(" ".join(temp_list[i].split()[3:]).strip('"'))
        else:
            continue
   else:
      tempvalues2.append(temp_list[i].split())

values2=np.array(tempvalues2)
values2=values2.astype(float)

concat=[]
count=0
for i in range(len(values)):
    concat.append([count,values[i][1],values[i][2]])
    count=count+2
for i in range(len(values2)):
    concat.append([count,values2[i][1],values2[i][2]])
    count=count+2


with open(sys.argv[3], 'w') as f:
    for i in range(len(concat)):
        f.write("%s\t%s\t%s\n" % (int(concat[i][0]), float(concat[i][1]),float(concat[i][2])) )
f.close


