#!/bin/bash

num_cluster=$1

rm -f centroids
for ((c=1;c<=$num_cluster;c++)); do
grep "     $c" ../GRID_ASSIGNATION > c${c}_GRID_ASSIGNATION2
python2 Py_CalcRepresentative_wt.py c${c}_GRID_ASSIGNATION2 >> centroids
done

python2 Py_AssignUnclustered_and_clustered.py > GRID_ASSIGNATION2_all
#cp GRID_ASSIGNATION2 GRID_ASSIGNATION2_clustered
#python2 Py_AssignUnclustered.py > GRID_ASSIGNATION2_unclustered
#cat GRID_ASSIGNATION2_unclustered >> GRID_ASSIGNATION2
