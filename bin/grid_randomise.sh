#!/bin/bash
#
# Run randomise to test z-statistic images.

if [[ $# -lt 1 ]]; then
    echo "randomise_new.sh fmdir"
    exit 1
fi


randomise -i /scratch/09123/ofriend/moshi/grid_coding/mni/new3/smoothed/masked_gm/group_z.nii.gz \
-o /scratch/09123/ofriend/moshi/grid_coding/mni/new3/smoothed/masked_gm/age_dec \
-d /scratch/09123/ofriend/moshi/grid_coding/randomise/new/age_decreasing.mat \
-t /scratch/09123/ofriend/moshi/grid_coding/randomise/new/age_decreasing.con \
-m /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/mni_gm_2mm_dil_masked.nii.gz \
-n 5000 -x --uncorrp


randomise -i /scratch/09123/ofriend/moshi/grid_coding/mni/new3/smoothed/masked_gm/group_z.nii.gz \
-o /scratch/09123/ofriend/moshi/grid_coding/mni/new3/smoothed/masked_gm/age_inc \
-d /scratch/09123/ofriend/moshi/grid_coding/randomise/new/age_increasing.mat \
-t /scratch/09123/ofriend/moshi/grid_coding/randomise/new/age_increasing.con \
-m /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/mni_gm_2mm_dil_masked.nii.gz \
-n 5000 -x --uncorrp

