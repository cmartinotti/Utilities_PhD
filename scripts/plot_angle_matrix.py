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
#read the file and fill the prob_matrix adding 1 every time a couple of angle occurs
for index, line in df.iterrows():
        prob_matrix[int(round(line["angle1"])),int(round(line["angle2"]))]+=1

#normalize the prob_matrix to sum up to 1
prob_matrix=prob_matrix/float(df.shape[0])

#prepare the reference matrix, 16381 is the number of slots inside the diamond.It has been obtained shamefully by
#counting the boxes with the following script:
counter =0
# for i in range(181):
#     for j in range(181):             #vTHIS DOWN HERE IS THE CONDITION OF EXISTENCE OF THE DIAMONDv
#         cond1=np.round(abs(np.deg2rad(i)-np.deg2rad(90)),4)
#         cond2=np.round(abs(np.deg2rad(j)-np.deg2rad(90)),4)
#         cond3=np.round(np.deg2rad(90),4)
#         if (np.round(cond1 + cond2,4) ) <= cond3: #diamond condition
#             counter+=1
# print counter

#this is because the ref_matrix has to have a flat probability in every slot, with an absolute value of
#NPOINTS/NOCCUPIEDSLOTS in every slot. Since the condition of existence is influenced by the numerical approximation
#i decided to count like an ape. So here is the ref_matrix:

ref_matrix=np.zeros((180,180))
for i in range(180):
    for j in range(180):
        if (abs(np.deg2rad(i) - np.deg2rad(90)) + abs(np.deg2rad(j)-np.deg2rad(90))) <= np.deg2rad(90):
            ref_matrix[i,j]=(float(df.shape[0])/16381)

#and here i normalize it
ref_matrix=ref_matrix/float(df.shape[0])
for i in range(180):
    for j in range(180):
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

#Here i impose the diamond existance condition, which would imply that the radicand is >=0, if this is true and then
#if the denominator is not zero i scale the value of prob_matrix by the analytical correction

        cond1=np.round(abs(np.deg2rad(i)-np.deg2rad(90)),4)
        cond2=np.round(abs(np.deg2rad(j)-np.deg2rad(90)),4)
        cond3=np.round(np.deg2rad(90),4)
        if (np.round(cond1 + cond2,4) ) <= cond3: #diamond condition, if this is true...

            cos2i=np.round((np.cos(np.deg2rad(i_ndex)))**2,4)
            cos2j=np.round((np.cos(np.deg2rad(j_ndex)))**2,4)
            sini=np.round(np.sin(np.deg2rad(i_ndex)),4)
            sinj=np.round(np.sin(np.deg2rad(j_ndex)),4)
            radicand=np.round(1-(cos2i+cos2j),4)
            denominator= sini*sinj
            if (denominator) != 0:                #...and this is true:
                prob_matrix[i,j]= prob_matrix[i,j] * np.sqrt(radicand)/denominator

flatness=0
diff_matrix=np.zeros((180,180))

for i in range(180):
    for j in range(180):
        diff_matrix[i,j]=(prob_matrix[i,j]-ref_matrix[i,j])**2
        flatness += np.sqrt(diff_matrix[i,j])
print flatness

dfmat=pd.DataFrame(prob_matrix)
data = [

    go.Surface(
        z=dfmat.as_matrix()
    )
]
layout = go.Layout(
    title=filein
)
fig = go.Figure(data=data, layout=layout)
py.offline.plot(fig)
