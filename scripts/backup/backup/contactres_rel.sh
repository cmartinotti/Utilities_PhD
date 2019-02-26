#!/bin/bash
#script che da la probabilita' di contatto tra due peptidi/proteine partendo dall output di g_mindist 

rm *.out  >/dev/null 2>&1
#g_mindist  -or   -s *.tpr  -n index.ndx -f traj.xtc   -respertime --> comando da usare, ricorda respertime
infile=$1 #file di input
val=$2  #valore di cutoff per l'interazione di legame
numres=$3 #numero residui
cat $infile | grep -v "[@,#]" >clean.out
lines=$(cat clean.out  | wc -l)
lines=$(($lines-1))
cat clean.out | tail -n $lines >clean2.out

for i in $(seq 1 $numres); do
col=$(($i+1))
cat clean2.out | gawk -v col=$col -v val=$val '{if ($col < val) print $col}' >>temp.out
done
lines=$(cat temp.out | wc -l)

rm 01.out >/dev/null 2>&1
for i in $(seq 1 $numres); do 
col=$(($i+1))
cat clean2.out | gawk -v col=$col -v val=$val '{if ($col < val) print $col}' >00.out
lines2=$(cat 00.out | wc -l)
echo $i $lines $lines2 | gawk '{print $1"  "($3/$2)}' >>01.out 

done
mv 01.out contact.xvg 

rm *.out
exit 0

