#FOR RUNNING IT FROM COMMAND LINE USE: gnuplot -e "filename='output.dat' ; outputname='1.8.pdf'" gnu_plot_new.sh
set title titlename noenhanced   		#if you dont put noenhanced the underscore is counter as a subscript
set style fill transparent solid 0.11 		#this is to set solid transparent so you can see the grid better
set style line 12 lc rgb 'black' lt 1 lw 1 	#grid width and syle
set xlabel  "{/Symbol Q}" font ",35" offset 0,-1.5 
set ylabel  "{/Symbol F}" font ",35" offset 0,-0.5
set zlabel  "Probability" font ",20" rotate by 90 offset -3.5
set xtics 30 font ",20" offset 0,-1.6				#major ticks
set ytics 30 font ",20" offset 3,-1 
set xrange [0:180]
set yrange [0:180]
set zrange [0:0.0012]
set xtics font ", 20"
set ytics font ", 20"
set ztics font ", 15"
set mxtics 2 					#medium ticks
set mytics 2
set grid xtics ytics mxtics mytics ls 12 	#plot the ticks on the grid
set ticslevel 0 				#offset of Z axis
set pm3d interpolate 0,0			#magic
set palette defined (0 '#ffffff', 1 '#e0ffff', 2 '#e0ffff', 3 '#afeeee', 4 '#40e0d0', 5 '#00ff7f', 6 '#7cff40', 7 '#a0ff20', 8 '#ffff00', 9 '#ffc020', 10 '#ff8040', 11 '#ff4500', 12 '#ff0000', 13 '#8b0000') #colori

set terminal png size 1000,1000
set terminal png transparent truecolor #pdf
set output outputname
splot  filename u 1:2:3 w pm3d notitle 		#notitle for the automatic stupid title which is th namedile

