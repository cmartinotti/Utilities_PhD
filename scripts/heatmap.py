#!/usr/bin/env python

import numpy as np
import sys
import getopt
import matplotlib.pyplot as pyp
import pandas as pd
import plotly as py
import plotly.offline as offline #import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go

filein=sys.argv[1]
df=pd.read_table(filein,skiprows=1 ,names=["time","angle1","angle2"])
prob_matrix=np.zeros((181,181))
for index, line in df.iterrows():
        prob_matrix[int(round(line["angle1"])),int(round(line["angle2"]))]+=1

prob_matrix=prob_matrix/float(df.shape[0])
for i in range(181):
    for j in range(181):
        if i == 0:
            i_ndex=0.25
        if j == 0:
            j_ndex=0.25
        if i == 180:
            i_ndex=179.75
        if j == 180:
            j_ndex=179.75
        else:
            i_ndex=i
            j_ndex=j

        radicand=(1-(np.cos(np.deg2rad(i_ndex))**2)-(np.cos(np.deg2rad(j_ndex))**2))
        if (abs(np.deg2rad(i) - np.deg2rad(90)) + abs(np.deg2rad(j)-np.deg2rad(90))) <= np.deg2rad(90):
            if radicand < 0:
                radicand=0
            if (np.sin(np.deg2rad(i_ndex))*np.sin(np.deg2rad(j_ndex))) != 0:
                prob_matrix[i,j]= prob_matrix[i,j] * np.sqrt(radicand)/(np.sin(np.deg2rad(i_ndex))*np.sin(np.deg2rad(j_ndex)))


dfmat=pd.DataFrame(prob_matrix)
mymat=dfmat.as_matrix()
print (np.std(mymat))
data = [
    go.Contour(
        z=mymat,
       )
]



layout = go.Layout(
    title=filein
)
fig = go.Figure(data=data, layout=layout)
py.offline.plot(fig)

