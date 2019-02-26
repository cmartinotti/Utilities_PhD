#!/bin/bash
infile=$1
column=$2

grep -v "@" $infile | grep -v "#" > temp.out

media=$( cat temp.out | awk -v col=$column '{sum1+=$col} END {print sum1/NR}')
echo media" "colonna=" "$media
stdev=$(awk -v media=$media -v col=$column '{sum +=( ($col-media) * ($col-media) ) } END {print sqrt(sum/NR)}' temp.out)
echo stdev" "colonna=" "$stdev
rm temp.out
