#!/usr/bin/env python
import pandas as pd
import os
import subprocess
import commands
import sys

#This program is used feeding it just the .log file of a simulation
os.system("grep \"Repl ex\" "+sys.argv[1]+ " >temp_probabilities.dat")

#Here i read the file and store the positional indices of all the Xs into an array of arrays
with open ('temp_probabilities.dat','r') as f:     #/standard reading part
    read_data=f.read()
f.close
temp_list=read_data.split('\n')

tempvalues=[]
all_indices=[]
for i in range(len(temp_list)-1):
    tempvalues.append(temp_list[i].split()) #finish of the standard reading part/
    tempvalues[i].pop(0)    #I eliminate the first 2 words cause i don't need them
    tempvalues[i].pop(0)
    indices= [n for n, m in enumerate(tempvalues[i]) if m == "x"] #This outputs the indices of every of the Xs
    all_indices.append(indices) #I store them into an array

#At this point though i have that in all_indices all the lines with n exchanges >1 has wrong indices, because
#every time there is an extra x, the number of character of the line increases by 1

#Beautiful part that fixes that problem
count=0
all_exchanges=[]
for i in range(len(all_indices)):
    for j in all_indices[i]:
        all_exchanges.append(j-count)
        count=count+1
    count=0

#This prints the probabilities
for i in range(1,int(tempvalues[0][-1])+1):
    print "probability of exchange ",i-1,"<->",i,float(all_exchanges.count(i))/float(len(all_indices)/2.0)," number of exchanges ",all_exchanges.count(i)

os.system("rm temp_probabilities.dat")
