proc align_membrane { grofile } {

# load .gro file
mol load gro $grofile


set popc [atomselect top "resname POPC"]
set toxin [atomselect top "not resname POPC"]

set gc_popc [geom_center $popc]
set gc_toxin [geom_center $toxin]

puts $gc_popc
puts $gc_toxin


#set matrix [measure fit $popc $toxin]
#set all [atomselect top "all" frame $k]
#$all move $matrix


set movevec [vecsub $gc_popc $gc_toxin]
$toxin moveby $movevec
$toxin moveby {0 0 52}

set all [atomselect top "all"]
$all writepdb popc_toxin_aligned.pdb

}


proc geom_center {selection} {
        
        # set the geometrical center to 0
        set gc [veczero]
        
        # [$selection get {x y z}] returns a list of {x y z} 
        #    values (one per atoms) so get each term one by one
        foreach coord [$selection get {x y z}] {
           
           # sum up the coordinates
           set gc [vecadd $gc $coord]
        
        }
        
        # and scale by the inverse of the number of atoms
        set gc_scaled [vecscale [expr 1.0 /[$selection num]] $gc]
        #puts $gc_scaled
        return $gc_scaled
}

proc center_of_mass {selection} {
        # some error checking
        if {[$selection num] <= 0} {
                error "center_of_mass: needs a selection with atoms"
        }
        # set the center of mass to 0
        set com [veczero]
        # set the total mass to 0
        set mass 0
        # [$selection get {x y z}] returns the coordinates {x y z} 
        # [$selection get {mass}] returns the masses
        # so the following says "for each pair of {coordinates} and masses,
	#  do the computation ..."
        foreach coord [$selection get {x y z}] m [$selection get mass] {
           # sum of the masses
           set mass [expr $mass + $m]
           # sum up the product of mass and coordinate
           set com [vecadd $com [vecscale $m $coord]]
        }
        # and scale by the inverse of the number of atoms
        if {$mass == 0} {
                error "center_of_mass: total mass is zero"
        }
        # The "1.0" can't be "1", since otherwise integer division is done
        return [vecscale [expr 1.0/$mass] $com]
}

align_membrane [lindex $argv 0] 

exit 
