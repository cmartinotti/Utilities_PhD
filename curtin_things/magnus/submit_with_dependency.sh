#!/bin/bash

#This is just a syntactically compact way to submit one job and his dependency  
job1_id=$(sbatch batch_gromacs_magnus.sh | cut -d " " -f 4);	# This line says "submit the job and take the number of the job that pops up from the command)                   
echo "Submitted batch job " $job1_id ; 				# Tell me you did submit it
sbatch --dependency=afterany:$job1_id batch_gromacs_magnus.sh	# Now submit another job with dependency on job1_id number. This can be replicated over and over for long chains.
