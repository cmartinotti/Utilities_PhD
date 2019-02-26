#!/usr/bin/env python

import numpy as np
import getopt, os, string, struct, sys
import matplotlib.pyplot as plt
from numpy import *

# Details about the programme
program_info = """ This program is a multipurpose one for analyzing lipids simulations:

- it can create  plots of XVG files which are saved in PDF file then

- calculate Area Per Lipid (APL) which is then saved in
 OUT text file and plotted in PDF file 

- compute the average repeated spacing of one lipid and surrounding medium in 
multibilayer systems; 

- compute the moving average of the input data with a chosen filtering window;

 ver. 1.1
"""

how_to_use = """\n\n The program should be used in the following manner:

    ./xvg_4_lipids.py [options] input.xvg output

NOTE: This programme works only with XVG files

Options for calculations:

--apl=          specifies area per lipid calculations and the number of 
                lipids in one leaflet (the result will be plotted automatically); 

--rep_space=    plots the average repeated spacing of a multibilayer lipid system for
                a specified number of bilayers stacked on each other; 

--movav=        calulates a moving average of a chosen property (APL, system's repeated spacing or just
                from the input data) with a specified window (the default unit is "ps");

--range=        defines in ns the starting time for the calculations of the mean values
                (APL and repeated spacing);

--fig           plots  data from the input file (only for time evolution which 
                is by default converted from [ps] to [ns]);

--title=        defines the title of the figure and should be written in apostrophes
                (e.g. 'title of the figure');

--labelx=       names the label of X-Axis and should be written in apostrophes
                (e.g. 'label Y of the figure'). The label for the X-coordinate
                is automatically chosen for APL calculations (i.e. 'time [$ps$ or [$ns$]]');

--labely=       names the label of Y-Axis and should be written in apostrophes
                (e.g. 'label Y of the figure'). The label for the Y-coordinate
                is automatically chosen for APL calculations (i.e. 'APL [$nm^2$]');

--xrange=      defines the range of x axis for which the data is plotted (e.g. --xrange=0,10) 

--yrange=      defines the range of y axis for which the data is plotted (e.g. --yrange=0,10)

--ns            changing the units of time to "ns" (default is "ps" ); 

"""


# Printing program info

print '\n'
print program_info
print how_to_use
print '\n'


# Reading options and files

try:
    options, files = getopt.getopt(sys.argv[1:], '',
                                       ['apl=','ns','movav=','fig','title=','labelx=','labely=','rep_space=','range=','xrange=','yrange='])
except getopt.GetoptError:
    sys.stderr.write(how_to_use)
    raise SystemExit

# Importing files
file_in, file_out = files

if not os.path.exists(file_in):
    sys.stderr.write('File %s not found\n' % file_in)
    raise SystemExit
else:
    data = np.loadtxt(file_in,skiprows=22,dtype=float)

if os.path.exists(file_out+'.pdf'):
    sys.stderr.write('File %s already exists. ' % file_out)
    while 1:
        overwrite = raw_input('Overwrite the file? [y/n]')
        if overwrite == 'n':
            raise SystemExit
        if overwrite == 'y':
            break


# Parameters check

global apl
apl = False
lip_no = None
global thick
thick = False
fig = False
moving = False
ps = 1.
descr = ''
unit = ''
titlename = ''
labelyname = ''
labelxname = ''
timerange = 0
x_range = False
y_range = False


for option, value in options:

    if option == '--ns':
         ps = 1000.

    if option == '--apl':
         lip_no = float(value)
         if lip_no < 0:
             sys.stderr.write("\nThe number of lipids must be larger than 0")
             sys.stderr.write(how_to_use)
             raise SystemExit
         apl = True

    if option == '--repeated spacing':
         bilayer_no = float(value)
         if bilayer_no < 0:
             sys.stderr.write("\nThe number of bilayers must be larger than 0")
             sys.stderr.write(how_to_use)
             raise SystemExit
         thick = True

    if option == '--movav':
         timestep2 = data[1,0]-data[0,0]
         window_value = float(value)
         window_length = int(window_value*ps/timestep2)
         if window_length < 0:
             sys.stderr.write("\nThe window size has to be larger than 0")
             sys.stderr.write(how_to_use)
             raise SystemExit
         moving = True

    if option == '--range':
         timestep = data[1,0]-data[0,0]
         timerange = int(float(value)*ps/timestep)
         if timerange < 0:
             sys.stderr.write("\nThe time can not be less than 0")
             sys.stderr.write(how_to_use)
             raise SystemExit

    if option == '--fig':
         fig = True

    if option == '--title':
         titlename = str(value)
         if titlename == 0:
             sys.stderr.write("\nYou must specify the title of the figure")
             sys.stderr.write(how_to_use)
             raise SystemExit

    if option == '--labely':
         labelyname = str(value)
         if labelyname == 0:
             sys.stderr.write("\nYou must specify the title of label for Y-axis")
             sys.stderr.write(how_to_use)
             raise SystemExit

    if option == '--labelx':
         labelxname = str(value)
         if labelxname == '':
             sys.stderr.write("\nYou must specify the title of label for X-axis\n")
             sys.stderr.write(how_to_use)
             raise SystemExit

    if option == '--xrange':
         x_range = True
         x_axis_range = map(float, string.split(value,','))
         if x_range == True:
             x_min = x_axis_range[0]*ps
             x_max = x_axis_range[1]*ps
             if x_min < 0 or x_max < 0: 
                 sys.stderr.write("\nThe plot range for X axis has to be larger than 0\n")
                 sys.stderr.write(how_to_use)
                 raise SystemExit

    if option == '--yrange':
         y_range = True
         y_axis_range = map(float, string.split(value,','))
         if y_range == True:
             y_min = y_axis_range[0]
             y_max = y_axis_range[1]
             if y_min < 0 or y_max < 0:
                 sys.stderr.write("\nThe plot range for Y axis has to be larger than 0\n")
                 sys.stderr.write(how_to_use)
                 raise SystemExit


# Functions

def CalcAPL(xvg_arr,lipids_no,outfile_name):
    # Calculating area per lipid
    APL=xvg_arr[:,1]*xvg_arr[:,1]/lipids_no
    APL_mean = round(np.mean(APL[timerange:]),5)
    APL_ARR=np.column_stack((xvg_arr[:,0],APL))
    # Calculating error of the APL as err=1.96*SD/(N^1/2) 
    APL_error=round(1.96*np.std(APL)/sqrt(len(APL)),5)
    # Saving APL in a text file
    outfile_header1 = 'This is a file with calculated Area Per Lipid (APL) from '+str(file_in)+'\n'
    outfile_header1 += 'The mean APL is '+str(APL_mean)+' +/- '+str(APL_error)+' [$nm^2$]\n\n'
    outfile_header1 += 'ps'+'      APL [$nm^2$]\n'
    np.savetxt(outfile_name+'.out',APL_ARR,header=outfile_header1,delimiter='\t',fmt='%s')
    return APL_ARR


def CalcThick(xvg_arr,bilayer_no,outfile_name):
    # Calculating area per lipid
    Thick=xvg_arr[:,1]/bilayer_no
    Thick_mean = round(np.mean(Thick[timerange:]),4)
    Thick_ARR=np.column_stack((xvg_arr[:,0],Thick))
    # Saving APL in a text file
    outfile_header2 = 'This is a file with calculated average repeated spacing of the system from '+str(file_in)+'\n'
    outfile_header2 += 'The mean repeated spacing is '+str(Thick_mean)+' [$nm$]\n\n'
    outfile_header2 += 'ps'+'      Thickness [$nm$]\n'
    np.savetxt(outfile_name+'.out',Thick_ARR,header=outfile_header2,delimiter='\t',fmt='%s')
    return Thick_ARR


def CalcMovAv(inp_arr,window_size,outfile_name): 
    # Calculating a  moving average
    window=np.ones(int(window_size))/float(window_size)
    MovingAverage=np.convolve(inp_arr[:,1],window,'same')
    MovAv_ARR=column_stack((inp_arr[:,0],MovingAverage))
    # Saving moving average in a text file
    if apl == True:
        descr = 'APL'
        unit = '[$nm^2$]'
    elif thick == True:
        descr = 'Thickness'
        unit = '[$nm$]'
    else:
        descr = labelyname
        unit = ''
    outfile_header3 = 'This is a file with calculated moving average of '+ descr +'\n'
    outfile_header3 += 'with the window size of '+ str(window_value*ps) +'ps'
    outfile_header3 += 'ns'+'      '+descr+' '+unit+'\n'
    np.savetxt(outfile_name+'_mov_av.out',MovAv_ARR,header=outfile_header3,delimiter='\t',fmt='%s')
    return MovAv_ARR


def PlotXVG(arr_inp,outfile_name,ps):
    # Plotting XVG data
    figXVG=plt.figure(figsize=(11.5, 7.5))
    mainbody=figXVG.add_subplot(111)
    mainbody.plot(arr_inp[:,0]/ps, arr_inp[:,1], 'b-', linewidth=1., label='plot')
    if x_range == True:
        mainbody.set_xlim(x_min, x_max)
    else:
        mainbody.set_xlim(0.0, np.amax(arr_inp[:,0]/ps))
    if y_range == True:
        mainbody.set_ylim(y_min,y_max)
    else:
        mainbody.set_ylim(np.amin(arr_inp[:,1])-0.15*np.mean(arr_inp[:,1]),
                          np.amax(arr_inp[:,1])+0.15*np.mean(arr_inp[:,1]))
    title=mainbody.set_title(titlename)
    title.set_size(20)
    if apl == True:
        laby=mainbody.set_ylabel(r'APL [$nm^2$]')
    elif thick == True:
        laby=mainbody.set_ylabel(r'Thickness [$nm$]')
    else:
        laby=mainbody.set_ylabel(labelyname)
    if ps == 1000.:
        labx=mainbody.set_xlabel(r'time [$ns$]')
    if (apl == True) or (thick == True):
        labx=mainbody.set_xlabel(r'time [$ps$]')
        if ps == 1000.:
             labx=mainbody.set_xlabel(r'time [$ns$]')
    else: 
        labx=mainbody.set_xlabel(labelxname)
    labx.set_size(18)
    laby.set_size(18)
    mainbody.tick_params(axis='both', which='major', labelsize=16)
    if x_range == True:
        text_x = x_min + (x_max-x_min)/2
    else:
        text_x = max(arr_inp[:,0]/(ps*2))
    if y_range == True:
        text_y = 0.95*y_max
    else:
        text_y = np.amax(arr_inp[:,1])+0.1*np.mean(arr_inp[:,1]) 
    plt.text(text_x,text_y,'Mean value = '+str(round(np.mean(arr_inp[:,1][timerange:]),5))+' +/- '+str(round(1.96*np.std(arr_inp[:,1][timerange:])/sqrt(len(arr_inp[:,1][timerange:])),5)),fontsize=15)
    if moving == True:
         Plot=figXVG.savefig(outfile_name+'_mov_av.pdf', dpi=900)
    else:
         Plot=figXVG.savefig(outfile_name+'.pdf', dpi=900)
    return Plot


# Program main


if apl == True and moving == False:
    APL_ARR=CalcAPL(data,lip_no,file_out)
    PlotXVG(APL_ARR,file_out,ps)


if apl == True and moving == True:
    APL_ARR=CalcAPL(data,lip_no,file_out)
    APL_movav=CalcMovAv(APL_ARR,window_length,file_out)
    PlotXVG(APL_movav,file_out,ps)


if thick == True and moving == False:
    Thick_ARR=CalcThick(data,bilayer_no,file_out)
    PlotXVG(Thick_ARR,file_out,ps)


if thick == True and moving == True:
    Thick_ARR=CalcThick(data,bilayer_no,file_out)
    Thick_movav=CalcMovAv(Thick_ARR,window_length,file_out)
    PlotXVG(Thick_movav,file_out,ps)


if moving == True and apl == False and thick == False:
    data_movav=CalcMovAv(data,window_length,file_out)
    PlotXVG(data_movav,file_out,ps)


if fig == True:
    PlotXVG(data,file_out,ps)

#KONIEC
