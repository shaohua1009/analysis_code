#!/bin/env bash

NX=100
NY=100
input=dihedrals.txt
TITLE="RSFF2 + TIP3P, BE-META, ${NX}x${NY} grids"

XMIN=-180.1
XMAX=180.1
YMIN=-180.1
YMAX=180.1
DEN_MAX=0.00016
FES_MAX=2.25

clean=0.00001
#clean=0
##########################################################################################
function calc_den () {
   den=${input/.txt/.den}
   echo "   Calcuting 2D density profile using input data: $input..."
   python2 Py_CalcDensity.py $input $XMIN $XMAX $YMIN $YMAX $NX $NY > $den

   allden=${input/.txt/_all.den}
   echo "   Calcuting 2D density profile using input data: $input..."
   python2 Py_CalcDensity.all.py $input $XMIN $XMAX $YMIN $YMAX $NX $NY > $allden

   den_png=${input/.txt/_den.png}
   echo "   Ploting the 2D Density using input data: $den ..."
   title="$TITLE, 2D density"
   gnuplot -e "TITLE='$title'; INPUT='$den'; XMIN='$XMIN'; XMAX='$XMAX'; YMIN='$YMIN'; YMAX='$YMAX'; DEN_MAX='$DEN_MAX'" Gp_PlotDensit2D.gplt
   convert -density 300 tmp.eps $den_png
}

##########################################################################################
function clean() {
   # Remove grids with density lower than pre-defined cutoff
   den=${input/.txt/.den}
   den2=${input/.txt/_kept.den}
   echo "   Removing grids with low density from data file: $den .."
   python2 Py_RemoveLowDensitGrids.py $den $clean > $den2

   den3=${input/.txt/_unclustered.den}
   echo "   Removing grids with high density that goes into clustering: $den .."
   python2 Py_RemoveHighDensitGrids.py $allden $clean > $den3

   den_png=${input/.txt/_keptden.png}
   echo "   Ploting the 2D Density using input data: $den ..."
   title="$TITLE, 2D density"
   gnuplot -e "TITLE='$title'; INPUT='$den2'; XMIN='$XMIN'; XMAX='$XMAX'; YMIN='$YMIN'; YMAX='$YMAX'; DEN_MAX='$DEN_MAX'" Gp_PlotKeptDensit2D.gplt
   convert -density 300 tmp.eps $den_png

   # Construct the distance matrix with kept grids 
   echo "   Constructing distance matrix using input data: $den2 ..."
   dmtx=${input/.txt/_kept.dmtx}
   python2 Py_CalcDistMatrixWithDensit.py $den2 > $dmtx
}

##########################################################################################
function calc_pop () {
   # Combine the Assignment file with density grids
   den2=${input/.txt/_kept.den}
   python2 Py_CombineDensitAndAssign.py $den2 CLUSTER_ASSIGNATION > GRID_ASSIGNATION
   # Plot the grid assignment without halo
   gcl_png=${input/.txt/_grid_cluster_v1.png}
   title="$TITLE, grid cluster"
   gnuplot -e "TITLE='$title'; INPUT='GRID_ASSIGNATION'; XMIN='$XMIN'; XMAX='$XMAX'; YMIN='$YMIN'; YMAX='$YMAX'" Gp_PlotGridCluster2D.gplt
   convert -density 300 tmp.eps $gcl_png

   # Calculate the population
   python2 Py_CalcPopFromGrid_v1.py $XMIN $XMAX $YMIN $YMAX $NX $NY

   # Plot the grid assignment according to the population
   gcl_png2=${input/.txt/_grid_cluster_v2.png}
   title="$TITLE, grid cluster"
   gnuplot -e "TITLE='$title'; INPUT='GRID_ASSIGNATION2'; XMIN='$XMIN'; XMAX='$XMAX'; YMIN='$YMIN'; YMAX='$YMAX'" Gp_PlotGridCluster2D.gplt
   convert -density 300 tmp.eps $gcl_png2
}

##########################################################################################
#calc_den #step1
#clean #step2
# Do cluster analysis using the kept grids
calc_pop &> populations.txt
