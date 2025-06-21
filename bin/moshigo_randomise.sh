#!/bin/bash
#
# Run randomise to test z-statistic images.

if [[ $# -lt 1 ]]; then
    echo "randomise_new.sh fmdir"
    exit 1
fi

sl_dir=$1

randomise -i ${sl_dir}/group_z.nii.gz \
-o ${sl_dir}/cont_last3 \
-d /scratch/09123/ofriend/moshi/grid_coding/randomise/int_design.mat \
-t /scratch/09123/ofriend/moshi/grid_coding/randomise/int_design.con \
-m /home1/09123/ofriend/analysis/moshigo_model/mni_gm_2mm.nii.gz \
-n 5000 -x --uncorrp

randomise -i ${sl_dir}/group_z.nii.gz \
-o ${sl_dir}/one_sample_last3 \
-m /home1/09123/ofriend/analysis/moshigo_model/mni_gm_2mm.nii.gz \
-1 \
-n 5000 -x  --uncorrp