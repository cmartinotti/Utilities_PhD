#!/usr/bin/env python

import numpy as np
from numpy import *
import os, sys, getopt, string
import matplotlib.pyplot as plt

# Program info
program_info = """ This program calculates the block standard error (BSE) of a given time-dependent 
quantity in the provided input file.
"""

how_to_use = """\n The program is used in the following manner:

      .block_average_xvg-0.3.py [options]

NOTE: works only with text files! 

The available options are:

--file=           specifies file name of the input file;

--range=          defines from which time the calculations are to be done;

--max_block=      specifies the maximal size of the block in decimal percentage 
                  of the total range of points for which the BSE is computed, e.g. 0.1 
                  means that the maximal block size will 10% of the total range of points 
                  which gives a standard error over 10 blocks (the default is 0.01
                  to have at least 100 points for statistically significant results);

--column=         defines which column in the input file contains the values for calculations
                  - the column ordering starts from '0' (the default is '1' which is the 2nd 
                  column - 1st column is expected to contain time); 

--ns              changes the units from [ps] to [ns] (assuming the unit for time in 
                  the input file is in [ps] ) 

ver. 1.1                  
"""


# Printing the program info

print '\n'
print program_info
print how_to_use

# Declare options
try:
     options, remainder = getopt.getopt(sys.argv[1:],'',['ns','file=','range=','max_block=','column='])
except getopt.GetoptErrorr:
     sys.stderr.write("\n DOES NOT COMPUTE! \n")
     sys.stderr.write(how_to_use)
     raise SystemExit


# Default parameters
unit = 1.0
UniT = '[ps]'
range = 0
max_block = 0.01
col = 1

# Declared options and files
for option, value in options:

     if option == '--ns':
          unit = 1000.
          UniT = '[ns]'

     if option == '--file':
          file_in = str(value)
          data = (line for line in open(file_in) if not line[0] in ('#','@','&','$'))
          data_full = np.loadtxt(data, dtype=float)
          if file_in == 0:
              sys.stderr.write("\n Without the input file there is not much to do...")
              sys.stderr.write(how_to_use)
              raise SystemExit

     if option == '--range':
          range = float(value)

     if option == '--max_block':
          max_block = float(value) # percent of the trajectory in decimal notation

     if option == '--column':
          column = int(value) 
          

# Reading in numerical data with the time range
time_step = data_full[1,0]-data_full[0,0]
time_range = int(range*unit/time_step) 
data_arr = data_full[time_range:-1]

 
# Loop and arrays inits
max_block_len = int(max_block*len(data_arr))
block_len = 1
stat_arr = np.empty([max_block_len-1,2],dtype=float)


# Block averaging 
while block_len < max_block_len:
     block_no = 0
     tot_blocks_no = int(len(data_arr)/block_len)
     valav_arr = np.empty([tot_blocks_no],dtype=float)
     while block_no < tot_blocks_no:
          valav_arr[block_no] = np.average(data_arr[block_no*block_len:(block_no+1)*block_len,col])
          block_no += 1
     stat_arr[block_len-1,0] = block_len*time_step/unit
     stat_arr[block_len-1,1] = round(np.std(valav_arr[:]/sqrt(len(valav_arr))),5)
     block_len += 1


# Plotting the results
fig=plt.figure(figsize=(11.5,7.5))
body=fig.add_subplot(111)

body.plot(stat_arr[:,0],stat_arr[:,1], linewidth=1.0)

title=body.set_title(file_in[:-4])
title.set_size(20)
labx=body.set_xlabel(r'Block size '+UniT)
labx.set_size(20)
laby=body.set_ylabel(r'BSE')
laby.set_size(20)

body.tick_params(axis='both', which='major', length=10, width=3, labelsize=18)
body.tick_params(axis='both', which='minor', length=5, width=1.5, labelsize=18)
body.minorticks_on()

fig.savefig(file_in[:-4]+'_block_average.pdf', dpi=900)


# Saving results in a text file 
comment = 'This is a calculation of a block standard error (BSE) of '+file_in[:-4]+'\n'
comment += 'block size '+UniT+'         BSE\n'

np.savetxt(file_in[:-4]+'_block_average.out', stat_arr, header=comment, delimiter='\t', fmt='%s')

##KONIEC
