#!/usr/bin/env python

import numpy as np
import MDAnalysis as mda

import sys
topol=sys.argv[1]
traj=sys.argv[2]

u=mda.Universe(topol, traj)

for ts in u.trajectory:
  pos6=np.array(list(u.select_atoms("bynum 6 10").positions[0]))  #select the atoms
  pos10=np.array(list(u.select_atoms("bynum 6 10").positions[1])) 
  pos7=np.array(list(u.select_atoms("bynum 7 15").positions[0]))
  pos15=np.array(list(u.select_atoms("bynum 7 15").positions[1]))
  vec_z= np.array([0,0,1])                           	#define z axis and vec1
  vec_1= np.array(pos10 - pos6)                      	#i now need a vec perpendicular to vec6-10 and to vec7-15
  vec_temp= np.array(pos15 - pos7)                   	#define a temporary vec7-15 for the cross product to find vec_2 
  vec_2= np.cross(vec_1,vec_temp)			#->remember here that a x b =! b x a, b x a = -a x b. So this vector should be pointing INTO the plane of the molecule
  norm_vec_z= np.sqrt(np.dot(vec_z, vec_z))		#the norms are for calculating the angles 
  norm_vec_1= np.sqrt(np.dot(vec_1, vec_1))
  norm_vec_2= np.sqrt(np.dot(vec_2, vec_2))
  angle_1=np.rad2deg(np.arccos((np.dot(vec_1,vec_z))/(norm_vec_1*norm_vec_z))) #angles are calculated with the formula
  angle_2=np.rad2deg(np.arccos((np.dot(vec_2,vec_z))/(norm_vec_2*norm_vec_z))) #to find an angle between 2 vectors
  
  f=open('angles.txt', 'a')                     #open the file with append option
  if ts.time == 0 :                            #if its the first step it empties the file
    f.seek(0)                                  #with this
    f.truncate()                               #and this line
  f.write("%s   %s   %s\n" % (int(ts.time), float(angle_1), float(angle_2))) #spaces are just left inbetween 
  f.close 
  #print(ts.time , "  ", angle_1,  file=f)    #it prints the required info but it require to import __future__


