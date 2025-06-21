#!/bin/bash
#
# Smooth functional data
subject=$1


module load python
module load afni

python acf_grid.py "${subject}"
