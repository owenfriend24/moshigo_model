#!/bin/bash
#
# Smooth functional data

if [[ $# -lt 1 ]]; then
    echo ""
    exit 1
fi

sl_dir=$1
sub=$2

cd ${sl_dir}/

#smooth_susan \
#    "${sl_dir}/cone/${sub}_60_ovr_30_mni_2mm_cone.nii.gz" \
#     "/home1/09123/ofriend/analysis/moshigo_model/mni_gm_2mm.nii.gz"\
#    4 \
#    "${sl_dir}/cone/smoothed_${sub}.nii.gz"
#echo "Finished smoothing run ${sub}!"
#
#smooth_susan \
#    "${sl_dir}/mountain/${sub}_60_ovr_30_mni_2mm_mountain.nii.gz" \
#     "/home1/09123/ofriend/analysis/moshigo_model/mni_gm_2mm.nii.gz"\
#    4 \
#    "${sl_dir}/mountain/smoothed_${sub}.nii.gz"
#echo "Finished smoothing run ${sub}!"


smooth_susan \
    "${sl_dir}/new4/${sub}_60_ovr_30_mni_2mm.nii.gz" \
     "/home1/09123/ofriend/analysis/moshigo_model/mni_gm_2mm.nii.gz"\
    4 \
    "${sl_dir}/new3/smoothed/${sub}_60_ovr_30_mni_2mm.nii.gz"
echo "Finished smoothing run ${sub}!"