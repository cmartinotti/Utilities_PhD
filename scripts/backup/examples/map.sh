#!/bin/bash
infile=$1

declare -A matrix
count=0

for ((i=0;i<181;i++))
do 
	for ((j=0;j<181;j++))
	do 
		matrix[$i,$j]=0; 
	done 
done





###############
while read line
do 
	teta=$(echo $line | awk '{print $2}') 
	phi=$(echo $line | awk '{print $3}') 
	roundedteta=$(printf "%.0f" "$teta" ) 
	roundedphi=$(printf "%.0f"  "$phi") 
	(( matrix[$roundedteta,$roundedphi]++ ))
	(( count++ ))
done < $infile

echo $count

for ((i=0;i<181;i++))
do
        for ((j=0;j<181;j++))
        do
                matrix[$i,$j]=$( echo "${matrix[$i,$j]}/($count)" | bc -l )
        done
done




#printf "\n\n\n"

for ((i=0;i<3;i++))
do
        for ((j=0;j<181;j++))
        do
                printf "%0.f  %f \n" "$i" "${matrix[$i,$j]}"
        done
        printf "\n"

done

#for ((i=0;i<10;i++))
#do
#        for ((j=0;j<10;j++))
#        do
#                printf "matrix[%.0f,%0.f]= %.0f " "$i" "$j" "${matrix[$i,$j]}"
#        done
#        printf "\n"
#
#done

