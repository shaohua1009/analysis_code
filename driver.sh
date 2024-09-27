#!/bin/bash
#Sx=$1
tail -n +13 phipsi_s1.xvg > txt1
tail -n +13 phipsi_s2.xvg > txt2
cat txt1 txt2 > dihedrals_sep_nohead.txt
rm txt1 txt2

size=$1
for ((i=1;i<=$size; i++)); do
mkdir residue$i
cd residue$i
dihed1=$((i*2+1))
dihed2=$((dihed1+1))
echo "awk '{print \$$dihed1,\$$dihed2}' ../dihedrals_sep_nohead.txt > dihedrals.txt "> awkcmd1
bash awkcmd1
cd ../
done

#cat residue1/dihedrals.txt residue2/dihedrals.txt residue3/dihedrals.txt residue4/dihedrals.txt residue5/dihedrals.txt residue6/dihedrals.txt residue7/dihedrals.txt > dihedrals.txt
cat residue*/dihedrals.txt >  dihedrals.txt
