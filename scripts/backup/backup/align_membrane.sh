#!/bin/bash
grofile=$1

/opt/vmd_1.9.2/vmd_1.9.2  -dispdev text -e /scripts/align_membrane.tcl -args $grofile

editconf -f popc_toxin_aligned.pdb -o popc_toxin_aligned.gro 

