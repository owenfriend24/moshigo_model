#!/bin/bash

if [[ $# -lt 1 ]]; then
    echo "Usage: manual_ashs_transforms.sh subject ashs_dir"

    exit 1
fi

sub=$1

ANTS 3 -m CC[/corral-repl/utexas/prestonlab/moshiGO1/${sub}/anatomy/brain.nii.gz, \
/corral-repl/utexas/prestonlab/moshiGO1/${sub}/anatomy/coronal_mean_brain.nii.gz,1,5] \
-t SyN[0.25] -r Gauss[3,0] -o /corral-repl/utexas/prestonlab/temple/moshigo/results/${sub}/NEW_coronal_to_anat_ \
-i 30x90x20 --use-Histogram-Matching \
--number-of-affine-iterations 10000x10000x10000x10000x10000 --MI-option 32x16000

#
#ANTS 3 -m MI[/corral-repl/utexas/prestonlab/moshiGO1/${sub}/anatomy/brain.nii.gz, \
#/corral-repl/utexas/prestonlab/moshiGO1/${sub}/anatomy/coronal_mean_brain.nii.gz, 1,32] \
#-t SyN[0.25] \
#-i 30x90x20 \
#-r Gauss[3,0] \
#-o /corral-repl/utexas/prestonlab/temple/moshigo/results/${sub}/NEW_coronal_to_anat_ --rigid-affine true -i 0
#
#
#antsApplyTransforms -d 3 \
#-i /corral-repl/utexas/prestonlab/moshiGO1/moshiGO_208/anatomy/L_ERC.nii.gz \
#-o L_ERC_in_func_space.nii.gz \
#-r /corral-repl/utexas/prestonlab/moshiGO1/moshiGO_208/anatomy/antsreg/data/funcunwarpspace/brain.nii.gz \
#-n NearestNeighbor \
#-t refvol2brain_Affine.txt \
#-t NEW_coronal_to_func_Affine.txt \
#-t NEW_coronal_to_func_Warp.nii.gz
