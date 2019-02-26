#!/bin/bash

#THIS SCRIPT IS USED TO PLOT THE 3D ANGLE PROBABILITIES MAP. YOU HAD TO MEASURE THE SINGLE ANGLE VS TIME FOR ANGLE1 AND ANGLE 2 AND THEN COMBINED IT INTO A SINGLE FILE, WHICH WILL BE THE IMPUT FOR THIS PROGRAM. EXPLANATION IN THE END.
#Example:		
#		map_awk 3_columns_file.dat

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



########SPIEGONE###########

# THIS SCRIPT CONSTRUCT AN 180x180 MATRIX  THEN COUNTS THE NUMBER OF TIME EACH COUPLE OF ANGLES OCCURS AND IN THE END DIVIDE BY THE NUMBER OF MEASURMENTS TO GIVE A DISTRIBUTION OF ANGLES WITH THEIR RESPECTIVE PROBABILITIES 

#infile=$1 							## INPUT FILE IN THE FORMAT OF A 3 COLUMN FILE WITH TIME(ps) ANGLE1 ANGLE2
#id=$(echo $infile | cut -d "_" -f 2 | cut -d "." -f 1,2)
#        awk ' 
#                BEGIN {
#                        for (i=0 ; i<181 ; i++) {		## 181 CAUSE THE DEGREES GOES FROM 0 TO 180 WITH G_GANGLE 
#                                for(j=0 ; j<181 ; j++) {
#                                        matrix[i][j]=0
#                                }
#                        }
#                count=0  
#                } 
#        
#
#                {
#                roundedteta=sprintf("%.0f", $2)                ## HERE SPRINTF IS USED TO ROUND THE VALUE OF $2 AND $3 TO 0 DECIMALS
#                roundedphi=sprintf("%.0f", $3)
#                matrix[roundedteta][roundedphi]++              ## HERE I INCREMENT THE VALUE OF THE MATRIX FROM THE COUPLE OF ANGLES THAT I JUST READ 
#                count++					## THIS IS THE COUNTER OF THE NUMBER OF MEASURMENTS (WHICH HAS TO BE THE NUMBER OF LINES OF THE FILE)
#                }
#
#                END {
#                        for (i=0 ; i<181 ; i++) {
#                                for(j=0 ; j<181 ; j++) {
#                                matrix[i][j]=matrix[i][j]/count## HERE I NORMALIZE THE PROBABILITIES BY THE NUMBER OF MEASURMENTS FOR THE WHOLE MATRIX
#                                }
#                        }
#
#
#                        for (i=0 ; i<181 ; i++) {
#                                for(j=0 ; j<181 ; j++) {
#                                        printf "%.0f %.0f  %-3f \n" ,i ,j ,matrix[i][j] ##HERE I PRINT THE MATRIX
#                                }
#                        printf "\n"				
#                        }
#                         
#                }       
#        ' $infile > output.dat					## AND I OUTPUT THE DATA IN OUTPUT.DAT
#
#gnuplot -e "filename='output.dat' ; outputname='map_$id.png' ; titlename='prob_map_$id'" /scripts/gnu_plot_new.sh #output.pdf ## HERE I CALL THE SCRIPT GNU_PLOT_NEW  THAT IS USED TO ACTUALLY CREATE THE IMAGES OF THE FILE IN OUTPUT.DAT
															       ## THE -e  FLAG IS TO PASS GNUPLOT THE VARIABLES (THE FILE NAME) 	

