#!/bin/bash
#
# grid transform

if [[ $# -lt 1 ]]; then
    echo "Usage: run_sl_transform.sh sub run"
    exit 1
fi

sub=$1

#if sub in ['']:
#warp_path="/corral-repl/utexas/prestonlab/temple/moshigo/results/${sub}/NEW_ANAT_to_mni2mm_Warp.nii.gz"
#affine_path="/corral-repl/utexas/prestonlab/temple/moshigo/results/${sub}/NEW_ANAT_to_mni2mm_Affine.txt"
#
#else:

if [[ "$sub" == "moshiGO_213" || "$sub" == "moshiGO_250" || "$sub" == "moshiGO_277" || "$sub" == "moshiGO_289" ]]; then
    warp_path="/corral-repl/utexas/prestonlab/temple/moshigo/results/${sub}/NEW_ANAT_to_mni2mm_Warp.nii.gz"
    affine_path="/corral-repl/utexas/prestonlab/temple/moshigo/results/${sub}/NEW_ANAT_to_mni2mm_Affine.txt"
else
#    warp_path="/corral-repl/utexas/prestonlab/temple/moshigo/results/${sub}/NEW_func_to_mni2mm_InverseWarp.nii.gz"
#    affine_path="/corral-repl/utexas/prestonlab/temple/moshigo/results/${sub}/NEW_func_to_mni2mm_Affine.txt"

    warp_path="/corral-repl/utexas/prestonlab/moshiGO1/${sub}/anatomy/antsreg/transforms/brain2MNI_func_Warp.nii.gz"
    affine_path="/corral-repl/utexas/prestonlab/moshiGO1/${sub}/anatomy/antsreg/transforms/brain2MNI_func_Affine.txt"
fi


antsApplyTransforms -d 3 \
    -i /scratch/09123/ofriend/moshi/grid_coding/${sub}/grid_data/${sub}_60_ovr_30_b_gray_dilated_z.nii.gz \
    -o /scratch/09123/ofriend/moshi/grid_coding/mni/new3/${sub}_60_ovr_30_mni_2mm.nii.gz \
    -r /home1/09123/ofriend/analysis/moshigo_model/bin/MNI152_T1_2mm_brain.nii.gz \
    -n NearestNeighbor \
    -t ${warp_path} \
    -t ${affine_path}

#antsApplyTransforms -d 3 \
#    -i /scratch/09123/ofriend/moshi/grid_coding/${sub}/grid_data/${sub}_60_ovr_30_erc_z.nii.gz \
#    -o /scratch/09123/ofriend/moshi/grid_coding/mni/erc/${sub}_60_ovr_30_mni_2mm_erc.nii.gz \
#    -r /home1/09123/ofriend/analysis/moshigo_model/bin/MNI152_T1_2mm_brain.nii.gz \
#    -n NearestNeighbor \
#    -t ${affine_path} \
#    -t ${warp_path}

#antsApplyTransforms -d 3 \
#    -i /scratch/09123/ofriend/moshi/grid_coding/${sub}/grid_data/${sub}_60_ovr_30_b_gray_dilated_cone_z.nii.gz \
#    -o /scratch/09123/ofriend/moshi/grid_coding/mni/cond/${sub}_60_ovr_30_mni_2mm_cone.nii.gz \
#    -r /home1/09123/ofriend/analysis/moshigo_model/bin/MNI152_T1_2mm_brain.nii.gz \
#    -n NearestNeighbor \
#    -t ${warp_path} \
#    -t ${affine_path}
#
#antsApplyTransforms -d 3 \
#    -i /scratch/09123/ofriend/moshi/grid_coding/${sub}/grid_data/${sub}_60_ovr_30_b_gray_dilated_mountain_z.nii.gz \
#    -o /scratch/09123/ofriend/moshi/grid_coding/mni/cond/${sub}_60_ovr_30_mni_2mm_mountain.nii.gz \
#    -r /home1/09123/ofriend/analysis/moshigo_model/bin/MNI152_T1_2mm_brain.nii.gz \
#    -n NearestNeighbor \
#    -t ${warp_path} \
#    -t ${affine_path}


echo "Transformed searchlight images to MNI space."
