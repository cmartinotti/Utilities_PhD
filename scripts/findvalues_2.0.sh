#!/bin/bash

number=$1
stride=$2
file=$3

treshold=0.005
#find the lines in the files with square minimums
findlines (){
awk -v number="$number" -v treshold="$treshold" -v stride="$stride" ' BEGIN {count_minus=count_plus=0}
{ 
if ((((number - stride) - $5)^2) < treshold ) {array_minus[count_minus,0]=$1 ; array_minus[count_minus,1]=$5 ; array_minus[count_minus,2]=(((number - stride) - $5)^2) ; count_minus=count_minus+1} 
if ((((number + stride) - $5)^2) < treshold ) {array_plus[count_plus,0]=$1 ; array_plus[count_plus,1]=$5 ; array_plus[count_plus,2]=(((number + stride) - $5)^2)  ; count_plus=count_plus+1 } 

  }
END {min_minus=min_plus=1
for (i = 0; i < count_minus; i++) { 
	if ( array_minus[i,2]< min_minus) {
		min_minus=array_minus[i,2]
		min_dist_minus=array_minus[i,1]
		frame_minus=array_minus[i,0] 
		}
}
for (i = 0; i < count_plus; i++) { 
	if ( array_plus[i,2]< min_plus) {
		min_plus=array_plus[i,2]
		min_dist_plus=array_plus[i,1]
		frame_plus=array_plus[i,0] 
		print array_plus[i,2]
		}
}

print frame_minus " " min_dist_minus 
print frame_plus  " " min_dist_plus
 }
' $file
}

findlines

