#!/usr/bin/env python

import numpy as np
import sys
import getopt
import pandas as pd

file=open(sys.argv[3],"r")

target=float(sys.argv[1])
stride=float(sys.argv[2])

treshold=0.005

row=[]
dist1=[]
dist2=[]
frame1=[]
frame2=[]
squaredist1=[]
squaredist2=[]
for line in file:
	row=[float(x) for x in line.split()]
	#row = line.split()
	if ( ((target - stride) - float(row[4]))**2  < treshold):
		dist1.append(float(row[4]))
		frame1.append(float(row[0]))
		squaredist1.append(((target - stride) - float(row[4]))**2) 

	elif ( ((target + stride) - float(row[4]))**2 < treshold):
		dist2.append(float(row[4]))
                frame2.append(float(row[0]))
		squaredist2.append(((target + stride) - row[4])**2) 
		#squaredist2.append(((target + stride) - float(row[4]))**2) 

frame1=np.array(frame1)
frame2=np.array(frame2)
dist1=np.array(dist1)
dist2=np.array(dist2)
squaredist1=np.array(squaredist1)
squaredist2=np.array(squaredist2)

df=pd.DataFrame({'frame': frame1,'dist':dist1,'sqrd':squaredist1 })
df2=pd.DataFrame({'frame': frame2,'dist':dist2,'sqrd':squaredist2 })
temp=[df.frame[df.sqrd.idxmin()] , df.dist[df.sqrd.idxmin()]]
temp2=[df2.frame[df2.sqrd.idxmin()] , df2.dist[df2.sqrd.idxmin()]]
print(' '.join(map(str, temp)))	
print(' '.join(map(str, temp2)))	
