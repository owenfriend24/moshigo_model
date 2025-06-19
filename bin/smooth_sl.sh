#!/bin/bash
#
# Smooth functional data

if [[ $# -lt 1 ]]; then
    echo ""
    exit 1
fi

sl_dir=$1

cd ${sl_dir}/

for sub in moshiGO*; do
    smooth_susan \
        "${sub}" \
         "/home1/09123/ofriend/analysis/moshigo_model/mni_gm_2mm.nii.gz"\
        4 \
        "smoothed_${sub}.nii.gz"

    echo "Finished smoothing run ${sub}!"

done