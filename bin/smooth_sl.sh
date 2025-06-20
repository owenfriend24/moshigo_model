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

smooth_susan \
    "${sl_dir}/${sub}_60_ovr_30_mni_2mm.nii.gz" \
     "/home1/09123/ofriend/analysis/moshigo_model/mni_gm_2mm.nii.gz"\
    4 \
    "${sl_dir}/smoothed_${sub}.nii.gz"
echo "Finished smoothing run ${sub}!"
