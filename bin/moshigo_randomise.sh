#!/bin/bash
#
# Run randomise to test z-statistic images.

if [[ $# -lt 1 ]]; then
    echo "randomise_new.sh fmdir"
    exit 1
fi

sl_dir=$1

randomise -i /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/new_group_z.nii.gz \
-o /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/age_increasing \
-d /scratch/09123/ofriend/moshi/grid_coding/randomise/age_increasing.mat \
-t /scratch/09123/ofriend/moshi/grid_coding/randomise/age_increasing.con \
-m /home1/09123/ofriend/analysis/moshigo_model/mni_gm_2mm.nii.gz \
-n 5000 -x --uncorrp

randomise -i /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/new_group_z.nii.gz \
-o /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/age_decreasing \
-d /scratch/09123/ofriend/moshi/grid_coding/randomise/age_decreasing.mat \
-t /scratch/09123/ofriend/moshi/grid_coding/randomise/age_decreasing.con \
-m /home1/09123/ofriend/analysis/moshigo_model/mni_gm_2mm.nii.gz \
-n 5000 -x --uncorrp

randomise -i /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/new_group_z.nii.gz \
-o /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/age_grouped \
-d /scratch/09123/ofriend/moshi/grid_coding/randomise/age_grouped.mat \
-t /scratch/09123/ofriend/moshi/grid_coding/randomise/age_grouped.con \
-m /home1/09123/ofriend/analysis/moshigo_model/mni_gm_2mm.nii.gz \
-n 5000 -x --uncorrp

randomise -i /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/new_group_z.nii.gz \
-o /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/performance \
-d /scratch/09123/ofriend/moshi/grid_coding/randomise/performance.mat \
-t /scratch/09123/ofriend/moshi/grid_coding/randomise/performance.con \
-m /home1/09123/ofriend/analysis/moshigo_model/mni_gm_2mm.nii.gz \
-n 5000 -x --uncorrp

randomise -i /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/new_group_z.nii.gz \
-o /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/one_sample_\
-m /home1/09123/ofriend/analysis/moshigo_model/mni_gm_2mm.nii.gz \
-1 \
-n 5000 -x  --uncorrp