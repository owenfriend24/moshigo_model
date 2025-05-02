#!/bin/bash

if [[ $# -lt 1 ]]; then
    echo "Usage: manual_ashs_transforms.sh subject ashs_dir"

    exit 1
fi

sub=$1

## create new warp/affine files for T1 to T2 transformation
ANTS 3 -m CC[/home1/09123/ofriend/analysis/temple/bin/templates/MNI152_T1_1mm_brain.nii.gz, \
/corral-repl/utexas/prestonlab/moshiGO1/${sub}/anatomy/antsreg/data/funcunwarpspace/brain.nii.gz,1,5] \
-t SyN[0.25] -r Gauss[3,0] -o $SCRATCH/moshi/pca_sl/results/${sub}/test_new_func_to_mni1mm_ \
-i 30x90x20 --use-Histogram-Matching \
--number-of-affine-iterations 10000x10000x10000x10000x10000 --MI-option 32x16000