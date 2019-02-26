#!/bin/bash

number=$1
treshold=$2
file=$3

#find the lines in the files with square minimums
findlines (){
awk -v find="$number" -v treshold="$treshold" ' BEGIN {counta=countb=countc=countd=0}
{ 
if (((find - 0.4) - $5)^2 < treshold && counta == 0) {print $0 ; counta=counta+1} 
if (((find - 0.2) - $5)^2 < treshold && countb == 0) {print $0 ; countb=countb+1} 
if (((find + 0.2) - $5)^2 < treshold && countc == 0) {print $0 ; countc=countc+1} 
if (((find + 0.4) - $5)^2 < treshold && countd == 0) {print $0 ; countd=countd+1} 

  }' $file
}

#store  arrays and counter
a=($(findlines | awk '{print $1 "\n"}' )) 
#b=($(findlines | awk '{printf "%.1f\n", $5 }' )) )  
b=($(findlines | awk '{print $5}' | cut -c 1-3 ))  
count=0

##extract frames
for i in ${a[@]};
do
echo 0 | trjconv -f clean.xtc -s ../*.tpr -dump $i -o ${b[$count]}.gro
#echo 1 13 | g_dist -f ${b[$count]}.gro -s ../*.tpr -o ${b[$count]}.xvg 
#grep -v [@,#] ${b[$count]}.xvg
count=$(($count + 1))
done
