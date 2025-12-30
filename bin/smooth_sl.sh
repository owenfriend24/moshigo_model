#!/bin/bash
#
# smooth functional z-maps

if [[ $# -lt 1 ]]; then
    echo ""
    exit 1
fi

sl_dir=$1
sub=$2

smooth_susan \
    "${sl_dir}/new3/${sub}_60_ovr_30_mni_2mm.nii.gz" \
     "/home1/09123/ofriend/analysis/moshigo_model/mni_gm_2mm.nii.gz"\
    4 \
    "${sl_dir}/new3/smoothed/${sub}_60_ovr_30_mni_2mm.nii.gz"
echo "Finished smoothing run ${sub}!"