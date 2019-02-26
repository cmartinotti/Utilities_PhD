#!/bin/bash

#NELL'INPUT FILE DEVONO ESSERE CONTENUTI IN QUEST'ORDINE
tpr="../topol.tpr" 		# 1 path del tpr
traj="../traj.trr" 		# 2 path del traj
index="../../index.ndx"     	# 3 path dell'index
gro=      	# 4 path del gro
skip=10	 	# 5 skip per pulire la traj se è troppo lunga
grp1=11     	# 6 gruppo1 di cui misurare le distanze con g_mindist 
grp2=12     	# 7 gruppo2 di cui misurare le distanze con g_mindist
cutoff=0.3    	# 8 cutoff per la distanza di legame
nres=182     	# 9 numero di residui del gruppo 1
nres2=75          # 9' numero di residui del gruppo 2
begin=100000    # 10 -b per l'equil
end=200000   	# 11 -e per l'equil
      		# 


for i in $(seq 1 6)
do
cd conf-$i
#cd conf-5
#mkdir analysis_carlo
cd analysis_carlo
pwd
#pulisci le traiettorie
#echo 1 1 | trjconv -s $tpr -f $traj -pbc cluster -ur compact -o pulita -skip $skip 
#echo 1 | trjconv -s $tpr -f pulita.xtc -dump 0 -ur compact -o 0.gro
#echo 1 1 | trjconv -s $tpr  -f pulita.xtc -pbc cluster -ur compact -o equilibrio -b $begin -e $end 

#RMSD
#echo 3 3 | g_rms -s 0.gro -f pulita.xtc 

#estrai le distanze di contatto e le probabilita' di contatto
echo  $grp1 $grp2 | g_mindist  -or contactres1-2.xvg   -s $tpr  -n $index -f equilibrio.xtc   -respertime  
echo  $grp2 $grp1 | g_mindist  -or contactres2-1.xvg   -s $tpr  -n $index -f equilibrio.xtc   -respertime

contactres_rel.sh contactres1-2.xvg $cutoff $nres
contactres_residue_mean_distance.sh contactres1-2.xvg $nres 
contactres_prob_absol contactres1-2.xvg $cutoff $nres 
mv contact_prob.xvg contact_prob1-2.xvg
mv contact.xvg contact1-2.xvg
mv contactres_relative_distance.xvg contactres_relative_distance1-2.xvg

contactres_rel.sh contactres2-1.xvg $cutoff $nres2
contactres_residue_mean_distance.sh contactres2-1.xvg $nres2 
contactres_prob_absol contactres2-1.xvg $cutoff $nres2 
mv contact_prob.xvg contact_prob2-1.xvg
mv contact.xvg contact2-1.xvg
mv contactres_relative_distance.xvg contactres_relative_distance2-1.xvg

cd ../../ 
pwd 
done

