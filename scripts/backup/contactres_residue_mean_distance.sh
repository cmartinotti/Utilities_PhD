#!/bin/bash

# script che, di base, esegue la media di tutte le colonne di un file colonna. Ad esempio calcola la media nel tempo della distanza minima di ogni residuo appartenente ad un gruppo dal gruppo partner, partendo dal file mindistres.xvg in uscita da g_mindist.
#NOTA i residui partono da 2 e arrivano fino a nres+1 perchè la prima colonna è il tempo e non ho voglia di corregere.

infile=$1
nres=$2

rm contactres_relative_distance.xvg

grep -v "#" $infile | grep -v "@" > temp.out
for i in $(seq 2 $(($nres+1)) )
do
	media=$(awk -v temp=$i '{sum+=$temp} END {print sum/NR}' temp.out)
	echo $i "  " $media "  " $(awk -v temp=$i -v media=$media '{dev+=($temp - media)*($temp - media)} END {print sqrt(dev/NR)}' temp.out) >> contactres_relative_distance.xvg
done
rm temp.out
