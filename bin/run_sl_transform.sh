#!/bin/bash
#
# run pca searchlight and transform to MNI space

if [[ $# -lt 2 ]]; then
    echo "run_sl_transform.sh sub mask"
    exit 1
fi

source /home1/09123/ofriend/analysis/temple/bin/profile

sub=$1
mask=$2

python pca_sl.py ${sub} ${mask}

for run in 1 2 3; do

  antsApplyTransforms -d 3 -i /scratch/09123/ofriend/moshi/pca_sl/results/${sub}/${sub}_run-${run}_pca12_varExpl.nii.gz \
  -o /scratch/09123/ofriend/moshi/pca_sl/results/${sub}/${sub}_run-${run}_pca12_varExpl_MNI.nii.gz \
  -r /home1/09123/ofriend/analysis/temple/bin/templates/MNI152_T1_1mm_brain.nii.gz \
  -n BSpline \
  -t /corral-repl/utexas/prestonlab/moshiGO1/${sub}/anatomy/antsreg/transforms/brain2MNI_1mm_Warp.nii.gz \
  -t /corral-repl/utexas/prestonlab/moshiGO1/${sub}/anatomy/antsreg/transforms/brain2MNI_1mm_Affine.txt
done
