#!/bin/bash

infile=$1
id=$(echo $infile | cut -d "_" -f 2 | cut -d "." -f 1,2)
	awk ' 
		BEGIN {
			for (i=0 ; i<181 ; i++) {
				for(j=0 ; j<181 ; j++) {
					matrix[i][j]=0
				}
			}
		count=0	 
		} 
	

		{
        	roundedteta=sprintf("%.0f", $2)
        	roundedphi=sprintf("%.0f", $3)
        	matrix[roundedteta][roundedphi]++
	        count++
		}

		END {
			for (i=0 ; i<181 ; i++) {
                                for(j=0 ; j<181 ; j++) {
                                matrix[i][j]=matrix[i][j]/count
				}
                        }


                        for (i=0 ; i<181 ; i++) {
                                for(j=0 ; j<181 ; j++) {
                                        printf "%.0f %.0f  %-3f \n" ,i ,j ,matrix[i][j]
                                }
			printf "\n"
                        }
                         
                } 	
	' $infile > output.dat

gnuplot -e "filename='output.dat' ; outputname='map_$id.png' ; titlename='prob_map_$id'" /scripts/gnu_plot_new.sh #output.pdf
