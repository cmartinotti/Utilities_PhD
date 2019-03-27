#!/bin/bash

#this programs needs a folder with all the name of the replicas that you want to launch named as WINDOW(COMdist)_COULscaling_VDWscaling and in the same superfolder all the itp, the gro and the topol with WINDOW COUL and VDW in places of the numbers. I'll usually store  those premade files except the gro  into a folder called basic_component

module load gromacs_magnus

#a counter used for lambdas
count=0 

#for every subfolder in this folder, this is also doable by for i in $(seq 0 0.2 X) for a more controlled manner
for i in $(ls -d */ | cut -d "/" -f 1) 
do
cd $i
cp ../*itp ../*.gro ../topol.top ../prod.mdp ../batch_gromacs_magnus.sh .    	# All these file with the proper formatting should be in the previous folder
window=$(echo $i | cut -d "_" -f 1)					     	#
coul=$(echo $i | cut -d "_" -f 2) 						# Get the variables 
vdw=$(echo $i | cut -d "_" -f 3)						#

sed -i "s/VDW/$vdw/g" topol.top							# Substitute the actual values in topol.top
sed -i "s/COUL/$coul/g" topol.top

sed -i "s/WINDOW/$window/g" prod.mdp						# And in the .mdp
if [ $((count%2)) == 0 ]
	then
	sed -i "s/LAMBDA/1.0/g" prod.mdp
	else
	sed -i "s/LAMBDA/0.999/g" prod.mdp
	fi
count=$((count+1))
rm pullf.xvg pullx.xvg state.cpt state_prev.cpt traj.xtc  traj.trr confout.gro ener.edr md.log # clean the eventual previous files. Be aware of this, cause you may don't want it
grompp_mpi -p topol.top -f prod.mdp -c *gro -maxwarn 1 				# grompps
pwd
delhash										# clean hashes
cd .. ;
done
