#!/bin/bash

if [[ $# -lt 1 ]]; then
    echo "Usage: manual_ashs_transforms.sh subject ashs_dir"

    exit 1
fi

sub=$1

#python $HOME/analysis/moshigo_model/bin/pca_cluster_model.py
#python $HOME/analysis/moshigo_model/bin/plot_pc_space.py
#python $HOME/analysis/moshigo_model/bin/extract_pc_embedding.py

## create new warp/affine files for T1 to T2 transformation
#ANTS 3 -m CC[/home1/09123/ofriend/analysis/temple/bin/templates/MNI152_T1_1mm_brain.nii.gz, \
#/corral-repl/utexas/prestonlab/moshiGO1/${sub}/anatomy/antsreg/data/funcunwarpspace/brain.nii.gz,1,5] \
#-t SyN[0.25] -r Gauss[3,0] -o /corral-repl/utexas/prestonlab/temple/moshigo/results/${sub}/test_new_func_to_mni1mm_ \
#-i 30x90x20 --use-Histogram-Matching \
#--number-of-affine-iterations 10000x10000x10000x10000x10000 --MI-option 32x16000

# for subject 285, 315
#ANTS 3 -m CC[/home1/09123/ofriend/analysis/moshigo_model/bin/MNI152_T1_2mm_brain.nii.gz, \
#/corral-repl/utexas/prestonlab/moshiGO1/${sub}/anatomy/coronal_mean_brain.nii.gz,1,5] \
#-t SyN[0.25] -r Gauss[3,0] -o /corral-repl/utexas/prestonlab/temple/moshigo/results/${sub}/NEW_CORONAL_to_mni2mm_ \
#-i 30x90x20 --use-Histogram-Matching \
#--number-of-affine-iterations 10000x10000x10000x10000x10000 --MI-option 32x16000

# fixed anat to func for subjects 213, 250, 277, 289
ANTS 3 -m CC[/corral-repl/utexas/prestonlab/moshiGO1/${sub}/anatomy/antsreg/data/funcunwarpspace/brain.nii.gz, \
/corral-repl/utexas/prestonlab/moshiGO1/${sub}/anatomy/brain.nii.gz,1,5] \
-t SyN[0.25] -r Gauss[3,0] -o /corral-repl/utexas/prestonlab/temple/moshigo/results/${sub}/NEW_ANAT_to_FUNC_ \
-i 30x90x20 --use-Histogram-Matching \
--number-of-affine-iterations 10000x10000x10000x10000x10000 --MI-option 32x16000



# normal T1w to MNI
#ANTS 3 -m CC[/home1/09123/ofriend/analysis/moshigo_model/bin/MNI152_T1_2mm_brain.nii.gz, \
#/corral-repl/utexas/prestonlab/moshiGO1/${sub}/anatomy/brain.nii.gz,1,5] \
#-t SyN[0.25] -r Gauss[3,0] -o /corral-repl/utexas/prestonlab/temple/moshigo/results/${sub}/NEW_ANAT_to_mni2mm_ \
#-i 30x90x20 --use-Histogram-Matching \
#--number-of-affine-iterations 10000x10000x10000x10000x10000 --MI-option 32x16000


#antsApplyTransforms -d 3 -i /corral-repl/utexas/prestonlab/moshiGO1/moshiGO_208/anatomy/L_ERC.nii.gz -o L_ERC_test.nii.gz \
#-r /corral-repl/utexas/prestonlab/moshiGO1/moshiGO_208/anatomy/antsreg/data/funcunwarpspace/brain.nii.gz \
#-n NearestNeighbor -t NEW_coronal_to_func_Warp.nii.gz -t NEW_coronal_to_func_Affine.txt -t refvol2brain_Affine.txt