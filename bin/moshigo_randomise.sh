#!/bin/bash
#
# Run randomise to test z-statistic images.

if [[ $# -lt 1 ]]; then
    echo "randomise_new.sh fmdir"
    exit 1
fi

sl_dir=$1

randomise -i /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/new_group_z.nii.gz \
-o /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/age_increasing \
-d /scratch/09123/ofriend/moshi/grid_coding/randomise/new/age_increasing.mat \
-t /scratch/09123/ofriend/moshi/grid_coding/randomise/new/age_increasing.con \
-m /home1/09123/ofriend/analysis/moshigo_model/mni_gm_2mm.nii.gz \
-n 5000 -x --uncorrp

randomise -i /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/new_group_z.nii.gz \
-o /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/age_decreasing \
-d /scratch/09123/ofriend/moshi/grid_coding/randomise/new/age_decreasing.mat \
-t /scratch/09123/ofriend/moshi/grid_coding/randomise/new/age_decreasing.con \
-m /home1/09123/ofriend/analysis/moshigo_model/mni_gm_2mm.nii.gz \
-n 5000 -x --uncorrp

randomise -i /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/new_group_z.nii.gz \
-o /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/age_grouped \
-d /scratch/09123/ofriend/moshi/grid_coding/randomise/new/age_grouped.mat \
-t /scratch/09123/ofriend/moshi/grid_coding/randomise/new/age_grouped.con \
-m /home1/09123/ofriend/analysis/moshigo_model/mni_gm_2mm.nii.gz \
-n 5000 -x --uncorrp

randomise -i /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/new_group_z.nii.gz \
-o /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/performance \
-d /scratch/09123/ofriend/moshi/grid_coding/randomise/new/performance.mat \
-t /scratch/09123/ofriend/moshi/grid_coding/randomise/new/performance.con \
-m /home1/09123/ofriend/analysis/moshigo_model/mni_gm_2mm.nii.gz \
-n 5000 -x --uncorrp

randomise -i /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/new_group_z.nii.gz \
-o /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/one_sample_new \
-m /home1/09123/ofriend/analysis/moshigo_model/mni_gm_2mm.nii.gz \
-1 \
-n 5000 -x  --uncorrp