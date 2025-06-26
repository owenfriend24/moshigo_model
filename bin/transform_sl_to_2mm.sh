#!/bin/bash
#
# grid transform

if [[ $# -lt 1 ]]; then
    echo "Usage: run_sl_transform.sh sub run"
    exit 1
fi

sub=$1


warp_path="/corral-repl/utexas/prestonlab/temple/moshigo/results/${sub}/NEW_func_to_mni2mm_Warp.nii.gz"
affine_path="/corral-repl/utexas/prestonlab/temple/moshigo/results/${sub}/NEW_func_to_mni2mm_Affine.txt"


antsApplyTransforms -d 3 \
    -i /scratch/09123/ofriend/moshi/grid_coding/${sub}/grid_data/${sub}_60_ovr_30_b_gray_dilated_cone_z.nii.gz \
    -o /scratch/09123/ofriend/moshi/grid_coding/mni/cond/${sub}_60_ovr_30_mni_2mm_cone.nii.gz \
    -r /home1/09123/ofriend/analysis/moshigo_model/bin/MNI152_T1_2mm_brain.nii.gz \
    -n NearestNeighbor \
    -t ${warp_path} \
    -t ${affine_path}

antsApplyTransforms -d 3 \
    -i /scratch/09123/ofriend/moshi/grid_coding/${sub}/grid_data/${sub}_60_ovr_30_b_gray_dilated_mountain_z.nii.gz \
    -o /scratch/09123/ofriend/moshi/grid_coding/mni/cond/${sub}_60_ovr_30_mni_2mm_mountain.nii.gz \
    -r /home1/09123/ofriend/analysis/moshigo_model/bin/MNI152_T1_2mm_brain.nii.gz \
    -n NearestNeighbor \
    -t ${warp_path} \
    -t ${affine_path}



#antsApplyTransforms -d 3 \
#    -i /scratch/09123/ofriend/moshi/grid_coding/${sub}/grid_data/${sub}_60_ovr_30_LATE_b_gray_dilated_last3_z.nii.gz \
#    -o /scratch/09123/ofriend/moshi/grid_coding/mni/${sub}_60_ovr_30_LATE_mni_2mm_last3.nii.gz \
#    -r /home1/09123/ofriend/analysis/moshigo_model/bin/MNI152_T1_2mm_brain.nii.gz \
#    -n NearestNeighbor \
#    -t ${warp_path} \
#    -t ${affine_path}

echo "Transformed searchlight images to MNI space."
