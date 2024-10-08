#!/bin/python

"""
python Py_write_dPCA_min_max.py all.txt #time_segment #clean
python Py_write_dPCA_min_max.py all.txt 50-100ns 0.05

This program reads s1s2_pc12.txt (combined s1 and s2 from dPCA) and writes two driver files
"""

import sys,os
import numpy as np
import math
import warnings

TIME=str(sys.argv[2])
CLEAN=float(sys.argv[3])

##########################################################

def read_lines(f):
   lines=[]
   for l in f: lines.append(l)
   return lines

def get_min_max(lines):
   x=[]
   y=[]
   z=[]
   for l in lines:
      spl=l.strip().split()
      x.append(float(spl[0]))
      y.append(float(spl[1]))
      warnings.filterwarnings("error")
      try:
         z.append(float(spl[2]))
      except:
         pass
   min_max=[]
   min_max.append(math.floor(min(x)))
   min_max.append(math.ceil(max(x)))
   min_max.append(math.floor(min(y)))
   min_max.append(math.ceil(max(y)))
   if3D = 0
   if z:
      if3D = 1
      min_max.append(math.floor(min(z)))
      min_max.append(math.ceil(max(z)))
   #print min_max
   return [min_max,if3D] 

##########################################################

def write_output(min_max,if3D):
   for i in ['s1','s2']:
      with open('driver_%s.sh'% (i),'w') as f:
         f.write('#!/bin/env bash\n\n')
         if if3D:
            f.write('NX=100\nNY=100\nNZ=100\n')
         else:
            f.write('NX=200\nNY=200\n')
         f.write('input=pc_projections.txt\n')
         if if3D:
            f.write('TITLE="RSFF2 + TIP3P, MD,%s %s, ${NX}x${NY}x${NZ} grids"\n\n'% (i,TIME))
         else:
            f.write('TITLE="RSFF2 + TIP3P, MD,%s %s, ${NX}x${NY} grids"\n\n'% (i,TIME))
         f.write('XMIN=%.1f\n'%(min_max[0]))
         f.write('XMAX=%.1f\n'%(min_max[1]))
         f.write('YMIN=%.1f\n'%(min_max[2]))
         f.write('YMAX=%.1f\n'%(min_max[3]))
         if if3D:
            f.write('ZMIN=%.1f\n'%(min_max[4]))
            f.write('ZMAX=%.1f\n'%(min_max[5]))
         f.write('DEN_MAX=5\nFES_MAX=2.25\n\n')
         f.write('clean=%.2f\n'% (CLEAN))
         f.write('##########################################################################################\n')
         f.write('function calc_den () {\n')
         f.write('   den=${input/.txt/.den}\n')
         f.write('   echo "   Calcuting 2D density profile using input data: $input..."\n')
         if if3D:
            f.write('   python Py_CalcDensity.py $input $XMIN $XMAX $YMIN $YMAX $ZMIN $ZMAX $NX $NY $NZ > $den\n\n')
            f.write('   den_png=${input/.txt/_den.png}\n')
            f.write('   echo "   Ploting the 2D Density using input data: $den ..."\n')
            f.write('   title="$TITLE, 2D density"\n')
            f.write("   gnuplot -e \"TITLE='$title'; INPUT='$den'; XMIN='$XMIN'; XMAX='$XMAX'; YMIN='$YMIN'; YMAX='$YMAX'; ZMIN='$ZMIN'; ZMAX='$ZMAX'; DEN_MAX='$DEN_MAX'\" Gp_PlotDensit3D.gplt\n")
         else:
            f.write('   python Py_CalcDensity.py $input $XMIN $XMAX $YMIN $YMAX $NX $NY > $den\n\n')
            f.write('   den_png=${input/.txt/_den.png}\n')
            f.write('   echo "   Ploting the 2D Density using input data: $den ..."\n')
            f.write('   title="$TITLE, 2D density"\n')
            f.write("   gnuplot -e \"TITLE='$title'; INPUT='$den'; XMIN='$XMIN'; XMAX='$XMAX'; YMIN='$YMIN'; YMAX='$YMAX'; DEN_MAX='$DEN_MAX'\" Gp_PlotDensit2D.gplt\n")
         f.write('   convert -density 300 tmp.eps $den_png\n')
         f.write('}\n\n')
         f.write('##########################################################################################\n')
         f.write('function clean() {\n')
         f.write('   # Remove grids with density lower than pre-defined cutoff\n')
         f.write('   den=${input/.txt/.den}\n')
         f.write('   den2=${input/.txt/_kept.den}\n')
         f.write('   echo "   Removing grids with 0 density from data file: $den .."\n')
         f.write('   python Py_RemoveLowDensitGrids.py $den $clean > $den2\n\n')
         f.write('   den_png=${input/.txt/_keptden.png}\n')
         f.write('   echo "   Ploting the 2D Density using input data: $den ..."\n')
         f.write('   title="$TITLE, 2D density"\n')
         if if3D:
            f.write("   gnuplot -e \"TITLE='$title'; INPUT='$den2'; XMIN='$XMIN'; XMAX='$XMAX'; YMIN='$YMIN'; YMAX='$YMAX'; ZMIN='$ZMIN'; ZMAX='$ZMAX'; DEN_MAX='$DEN_MAX'\" Gp_PlotKeptDensit3D.gplt\n")
         else:
            f.write("   gnuplot -e \"TITLE='$title'; INPUT='$den2'; XMIN='$XMIN'; XMAX='$XMAX'; YMIN='$YMIN'; YMAX='$YMAX'; DEN_MAX='$DEN_MAX'\" Gp_PlotKeptDensit2D.gplt\n")
         f.write('   convert -density 300 tmp.eps $den_png\n\n')
         f.write('   # Construct the distance matrix with kept grids \n')
         f.write('   echo "   Constructing distance matrix using input data: $den2 ..."\n')
         f.write('   dmtx=${input/.txt/_kept.dmtx}\n')
         f.write('   python Py_CalcDistMatrixWithDensit.py $den2 > $dmtx\n')
         f.write('}\n\n')
         f.write('##########################################################################################\n')
         f.write('function calc_pop () {\n')
         f.write('   # Combine the Assignment file with density grids\n')
         f.write('   den2=${input/.txt/_kept.den}\n')
         f.write('   python Py_CombineDensitAndAssign.py $den2 CLUSTER_ASSIGNATION > GRID_ASSIGNATION\n')
         f.write('   # Plot the grid assignment without halo\n')
         f.write('   gcl_png=${input/.txt/_grid_cluster_v1.png}\n')
         f.write('   title="$TITLE, grid cluster"\n')
         if if3D:
            f.write("   gnuplot -e \"TITLE='$title'; INPUT='GRID_ASSIGNATION'; XMIN='$XMIN'; XMAX='$XMAX'; YMIN='$YMIN'; YMAX='$YMAX'; ZMIN='$ZMIN'; ZMAX='$ZMAX'\" Gp_PlotGridCluster3D.gplt\n")
         else:
            f.write("   gnuplot -e \"TITLE='$title'; INPUT='GRID_ASSIGNATION'; XMIN='$XMIN'; XMAX='$XMAX'; YMIN='$YMIN'; YMAX='$YMAX'\" Gp_PlotGridCluster2D.gplt\n")
         f.write('   convert -density 300 tmp.eps $gcl_png\n\n')
         f.write('   # Calculate the population\n')
         if if3D:
            f.write('   python Py_CalcPopFromGrid_v1.py $XMIN $XMAX $YMIN $YMAX $ZMIN $ZMAX $NX $NY $NZ\n\n')
         else:
            f.write('   python Py_CalcPopFromGrid_v1.py $XMIN $XMAX $YMIN $YMAX $NX $NY\n\n')
         f.write('   # Plot the grid assignment according to the population\n')
         f.write('   gcl_png2=${input/.txt/_grid_cluster_v2.png}\n')
         f.write('   title="$TITLE, grid cluster"\n')
         if if3D:
            f.write("   gnuplot -e \"TITLE='$title'; INPUT='GRID_ASSIGNATION2'; XMIN='$XMIN'; XMAX='$XMAX'; YMIN='$YMIN'; YMAX='$YMAX'; ZMIN='$ZMIN'; ZMAX='$ZMAX'\" Gp_PlotGridCluster3D.gplt\n")
         else:
            f.write("   gnuplot -e \"TITLE='$title'; INPUT='GRID_ASSIGNATION2'; XMIN='$XMIN'; XMAX='$XMAX'; YMIN='$YMIN'; YMAX='$YMAX'\" Gp_PlotGridCluster2D.gplt\n")
         f.write('   convert -density 300 tmp.eps $gcl_png2\n')
         f.write('}\n\n')
         f.write('##########################################################################################\n')
         f.write('calc_den #step1\n')
         f.write('clean #step2\n')
         f.write('# Do cluster analysis using the kept grids\n')
         f.write('#calc_pop &> populations.txt\n')

##########################################################

def main():
   with open(sys.argv[1],'r') as f:
      lines=read_lines(f)
   min_max,if3D=get_min_max(lines)
   print (min_max, if3D)
   write_output(min_max,if3D)

if __name__ == '__main__': 
   main()
