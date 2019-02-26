#!/usr/bin/env python
import xvgstuff
import pandas as pd
import numpy as np
import sys
import os


sys.stderr.write("use like " + sys.argv[0]+ " file.xvg distance. It returns the number of the frame and the actual z absolute distance \n") 
df=xvgstuff.xvgtotable(sys.argv[1])
neigh=df[np.sqrt((float(sys.argv[2])-df.iloc[:,4])**2)<0.1].iloc[0,[0,4]].values
#neigh=df[np.sqrt((float(sys.argv[2])-df.iloc[:,4])**2)<0.01].iloc[0,[0,4]].values
if (neigh.any()):
    print(neigh[0].astype(int))




