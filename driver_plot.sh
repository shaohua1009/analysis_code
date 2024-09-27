XMIN=-180.1
XMAX=180.1
YMIN=-180.1
YMAX=180.1
DEN_MAX=0.00016
FES_MAX=2.25

NX=100
NY=100
input=dihedrals.txt
TITLE="RSFF2 + TIP3P, BE-META, ${NX}x${NY} grids"

den2=dihedrals_kept.den
den=dihedrals.den
gnuplot -e "TITLE='$title'; INPUT='$den'; XMIN='$XMIN'; XMAX='$XMAX'; YMIN='$YMIN'; YMAX='$YMAX'; DEN_MAX='$DEN_MAX'" Gp_PlotKeptDensit2D.gplt
#convert -density 300 tmp.eps $den_png

