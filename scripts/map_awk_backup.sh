#!/bin/bash

infile=$1
id=$(echo $infile | cut -d "_" -f 2 | cut -d "." -f 1,2)
	awk ' 
		BEGIN {
			for (i=0 ; i<181 ; i++) {
					teta[i]=0
					phi[i]=0
				}
			
		count=0	 
		} 
	

		{
        	roundedteta=sprintf("%.0f", $2)
        	roundedphi=sprintf("%.0f", $3)
        	teta[roundedteta]++
		phi[roundedphi]++
	        count++
		}

		END {
			for (i=0 ; i<181 ; i++) {
                                phi[i]=phi[i]/count
                                teta[i]=teta[i]/count
                        }


                        for (i=0 ; i<181 ; i++) {
                                        printf "%.0f %-3f %-3f \n" ,i ,phi[i],teta[i]
			printf "\n"
                        }
                         
                } 	
	' $infile > output.dat

