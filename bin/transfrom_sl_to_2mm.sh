#!/bin/bash
#
# grid transform

if [[ $# -lt 2 ]]; then
    echo "Usage: run_sl_transform.sh sub run"
    exit 1
fi

sub=$1

# Handle special cases for certain subjects
if [[ "$sub" == "moshiGO_250" || "$sub" == "moshiGO_230" || "$sub" == "moshiGO_285" || "$sub" == "moshiGO_334" || "$sub" == "moshiGO_277" ]]; then
    warp_path="/corral-repl/utexas/prestonlab/temple/moshigo/results/${sub}/test_new_func_to_mni1mm_Warp.nii.gz"
    affine_path="/corral-repl/utexas/prestonlab/temple/moshigo/results/${sub}/test_new_func_to_mni1mm_Affine.txt"
else
    warp_path="/corral-repl/utexas/prestonlab/moshiGO1/${sub}/anatomy/antsreg/transforms/brain2MNI_1mm_Warp.nii.gz"
    affine_path="/corral-repl/utexas/prestonlab/moshiGO1/${sub}/anatomy/antsreg/transforms/brain2MNI_1mm_Affine.txt"
fi

antsApplyTransforms -d 3 \
    -i /scratch/09123/ofriend/moshi/grid_coding/${sub}/grid_data/${sub}_60_ovr_30_b_gray_dilated_z.nii.gz \
    -o /scratch/09123/ofriend/moshi/grid_coding/mni/${sub}_60_ovr_30_mni_2mm.nii.gz \
    -r /home1/09123/ofriend/analysis/temple/bin/templates/MNI152_T1_2mm_brain.nii.gz \
    -n NearestNeighbor \
    -t ${warp_path} \
    -t ${affine_path}

echo "Transformed searchlight images to MNI space."
