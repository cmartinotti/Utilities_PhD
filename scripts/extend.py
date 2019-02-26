#!/usr/bin/env python

import pandas as pd
import re
import sys
import os
import subprocess
import commands

wheresh="/home/cmartinotti/scripts/where.sh"
out_wheresh=commands.getstatusoutput(wheresh)
data=[]
for i in range(len(out_wheresh[1].split('\n'))):
    data.append(out_wheresh[1].split('\n')[i].split())

df=pd.DataFrame(columns=data[0], data=data[1:])

df.dropna(axis=0,inplace=True)
elim=df.loc[df['Reason']=='Dependency']['WorkDir'].values[:]

for i in range(len(elim)):
    df=df[df['WorkDir']!=elim[i]]
df.reset_index(drop=True)
list_relaunch=[]
for i in range(len(df)):
    list_relaunch.append(df.iloc[i,[0,8]].values)

for i in range(len(list_relaunch)):
    os.chdir(list_relaunch[i][1])
    if os.path.isfile(list_relaunch[i][1]+"/batch_gromacs_magnus.sh"):
	cmd = "sbatch --dependency=afterany:" + list_relaunch[i][0] + " batch_gromacs_magnus.sh"
	print "Submitting Job1 with command: %s" % cmd
	status, jobnum = commands.getstatusoutput(cmd)
	if (status == 0 ):
	    print "Job1 is %s" % jobnum
	    print cmd
	else:
    	    print "Error submitting Job1"
    elif os.path.isfile(list_relaunch[i][1]+"/batch_regular.sh"):
	cmd = "sbatch --dependency=afterany:" + list_relaunch[i][0] + " batch_regular.sh"
	print "Submitting Job1 with command: %s" % cmd
	cmd
	status, jobnum = commands.getstatusoutput(cmd)
	if (status == 0 ):
	    print "Job1 is %s" % jobnum
	else:
	    print "Error submitting Job1"
    else :
        print ("something wrong with the directory " + list_relaunch[i][1] + " , can't find the batch script." )
    
