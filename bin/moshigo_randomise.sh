#!/bin/bash
#
# Run randomise to test z-statistic images.

if [[ $# -lt 1 ]]; then
    echo "randomise_new.sh fmdir"
    exit 1
fi

sl_dir=$1

randomise -i /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/adult_z.nii.gz \
-o /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/one_sample_adult \
-m /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/mni_gm_2mm_dil_masked.nii.gz \
-1 \
-n 5000 -x  --uncorrp

randomise -i /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/child_z.nii.gz \
-o /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/one_sample_child \
-m /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/mni_gm_2mm_dil_masked.nii.gz \
-1 \
-n 5000 -x  --uncorrp

#randomise -i /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/new_group_z.nii.gz \
#-o /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/age_increasing \
#-d /scratch/09123/ofriend/moshi/grid_coding/randomise/new/age_increasing.mat \
#-t /scratch/09123/ofriend/moshi/grid_coding/randomise/new/age_increasing.con \
#-m /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/mni_gm_2mm_dil_masked.nii.gz \
#-n 5000 -x --uncorrp
#
#randomise -i /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/new_group_z.nii.gz \
#-o /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/age_decreasing \
#-d /scratch/09123/ofriend/moshi/grid_coding/randomise/new/age_decreasing.mat \
#-t /scratch/09123/ofriend/moshi/grid_coding/randomise/new/age_decreasing.con \
#-m /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/mni_gm_2mm_dil_masked.nii.gz \
#-n 5000 -x --uncorrp
#
#randomise -i /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/new_group_z.nii.gz \
#-o /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/age_grouped \
#-d /scratch/09123/ofriend/moshi/grid_coding/randomise/new/age_grouped.mat \
#-t /scratch/09123/ofriend/moshi/grid_coding/randomise/new/age_grouped.con \
#-m /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/mni_gm_2mm_dil_masked.nii.gz \
#-n 5000 -x --uncorrp
#
#randomise -i /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/new_group_z.nii.gz \
#-o /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/performance \
#-d /scratch/09123/ofriend/moshi/grid_coding/randomise/new/performance.mat \
#-t /scratch/09123/ofriend/moshi/grid_coding/randomise/new/performance.con \
#-m /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/mni_gm_2mm_dil_masked.nii.gz \
#-n 5000 -x --uncorrp
#
#randomise -i /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/new_group_z.nii.gz \
#-o /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/performance_inverse \
#-d /scratch/09123/ofriend/moshi/grid_coding/randomise/new/performance.mat \
#-t /scratch/09123/ofriend/moshi/grid_coding/randomise/new/performance_inverse.con \
#-m /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/mni_gm_2mm_dil_masked.nii.gz \
#-n 5000 -x --uncorrp
#
#randomise -i /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/new_group_z.nii.gz \
#-o /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/imp_score \
#-d /scratch/09123/ofriend/moshi/grid_coding/randomise/new/imp_score.mat \
#-t /scratch/09123/ofriend/moshi/grid_coding/randomise/new/imp_score.con \
#-m /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/mni_gm_2mm_dil_masked.nii.gz \
#-n 5000 -x --uncorrp
#
#randomise -i /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/new_group_z.nii.gz \
#-o /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/one_sample_new \
#-m /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/mni_gm_2mm_dil_masked.nii.gz \
#-1 \
#-n 5000 -x  --uncorrp