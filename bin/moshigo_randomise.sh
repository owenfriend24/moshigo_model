#!/bin/bash
#
# Run randomise to test z-statistic images.

if [[ $# -lt 1 ]]; then
    echo "randomise_new.sh fmdir"
    exit 1
fi

cond=$1

# /scratch/09123/ofriend/moshi/grid_coding/mni/new3/smoothed/masked/new_group_z.nii.gz

randomise -i /scratch/09123/ofriend/moshi/grid_coding/mni/new3/smoothed/smooth_group_z.nii.gz \
-o /scratch/09123/ofriend/moshi/grid_coding/mni/new3/smoothed/age_dec \
-d /scratch/09123/ofriend/moshi/grid_coding/randomise/new/age_decreasing.mat \
-t /scratch/09123/ofriend/moshi/grid_coding/randomise/new/age_decreasing.con \
-m /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/mni_gm_2mm_dil_masked.nii.gz \
-n 5000 -x --uncorrp

randomise -i /scratch/09123/ofriend/moshi/grid_coding/mni/new3/smoothed/smooth_group_z.nii.gz \
-o /scratch/09123/ofriend/moshi/grid_coding/mni/new3/smoothed/age_dec2 \
-d /scratch/09123/ofriend/moshi/grid_coding/randomise/new/age_decreasing.mat \
-t /scratch/09123/ofriend/moshi/grid_coding/randomise/new/age_decreasing.con \
-m /home1/09123/ofriend/analysis/moshigo_model/mni_gm_2mm.nii.gz \
-n 5000 -x --uncorrp




randomise -i /scratch/09123/ofriend/moshi/grid_coding/mni/new3/smoothed/masked_gm/group_z.nii.gz \
-o /scratch/09123/ofriend/moshi/grid_coding/mni/new3/smoothed/masked_gm/age_dec \
-d /scratch/09123/ofriend/moshi/grid_coding/randomise/new/age_decreasing.mat \
-t /scratch/09123/ofriend/moshi/grid_coding/randomise/new/age_decreasing.con \
-m /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/mni_gm_2mm_dil_masked.nii.gz \
-n 5000 -x --uncorrp


randomise -i /scratch/09123/ofriend/moshi/grid_coding/mni/new3/smoothed/masked_wb/group_z.nii.gz \
-o /scratch/09123/ofriend/moshi/grid_coding/mni/new3/smoothed/masked_wb/age_dec \
-d /scratch/09123/ofriend/moshi/grid_coding/randomise/new/age_decreasing.mat \
-t /scratch/09123/ofriend/moshi/grid_coding/randomise/new/age_decreasing.con \
-m /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/mni_gm_2mm_dil_masked.nii.gz \
-n 5000 -x --uncorrp

#-m /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/mni_gm_2mm_dil_masked.nii.gz

#randomise -i /scratch/09123/ofriend/moshi/grid_coding/mni/erc/smoothed/group_z.nii.gz \
#-o /scratch/09123/ofriend/moshi/grid_coding/mni/erc/smoothed/age_param \
#-d /scratch/09123/ofriend/moshi/grid_coding/mni/erc/randomise_age.mat \
#-t /scratch/09123/ofriend/moshi/grid_coding/mni/erc/randomise_age.con \
#-m /scratch/09123/ofriend/moshi/grid_coding/mni/erc/masks/group_mask_fix.nii.gz \
#-n 5000 -x --uncorrp
#
#randomise -i /scratch/09123/ofriend/moshi/grid_coding/mni/erc/smoothed/group_z.nii.gz \
#-o /scratch/09123/ofriend/moshi/grid_coding/mni/erc/smoothed/one_sample_new \
#-m /scratch/09123/ofriend/moshi/grid_coding/mni/erc/masks/group_mask_fix.nii.gz \
#-1 \
#-n 5000 -x  --uncorrp

#randomise -i /scratch/09123/ofriend/moshi/grid_coding/mni/cond/mountain/smoothed/mountain_group_z.nii.gz \
#-o /scratch/09123/ofriend/moshi/grid_coding/mni/cond/mountain/smoothed/age_decreasing \
#-d /scratch/09123/ofriend/moshi/grid_coding/randomise/new/age_decreasing.mat \
#-t /scratch/09123/ofriend/moshi/grid_coding/randomise/new/age_decreasing.con \
#-m /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/mni_gm_2mm_dil_masked.nii.gz \
#-n 5000 -x --uncorrp
#
#randomise -i /scratch/09123/ofriend/moshi/grid_coding/mni/cond/mountain/smoothed/mountain_group_z.nii.gz \
#-o /scratch/09123/ofriend/moshi/grid_coding/mni/cond/mountain/smoothed/age_grouped \
#-d /scratch/09123/ofriend/moshi/grid_coding/randomise/new/age_grouped.mat \
#-t /scratch/09123/ofriend/moshi/grid_coding/randomise/new/age_grouped.con \
#-m /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/mni_gm_2mm_dil_masked.nii.gz \
#-n 5000 -x --uncorrp
#
#randomise -i /scratch/09123/ofriend/moshi/grid_coding/mni/cond/cone/smoothed/cone_group_z.nii.gz \
#-o /scratch/09123/ofriend/moshi/grid_coding/mni/cond/cone/smoothed/age_increasing \
#-d /scratch/09123/ofriend/moshi/grid_coding/randomise/new/age_increasing_cone.mat \
#-t /scratch/09123/ofriend/moshi/grid_coding/randomise/new/age_increasing_cone.con \
#-m /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/mni_gm_2mm_dil_masked.nii.gz \
#-n 5000 -x --uncorrp
#
#randomise -i /scratch/09123/ofriend/moshi/grid_coding/mni/cond/cone/smoothed/cone_group_z.nii.gz \
#-o /scratch/09123/ofriend/moshi/grid_coding/mni/cond/cone/smoothed/age_decreasing \
#-d /scratch/09123/ofriend/moshi/grid_coding/randomise/new/age_decreasing_cone.mat \
#-t /scratch/09123/ofriend/moshi/grid_coding/randomise/new/age_decreasing_cone.con \
#-m /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/mni_gm_2mm_dil_masked.nii.gz \
#-n 5000 -x --uncorrp
#
#randomise -i /scratch/09123/ofriend/moshi/grid_coding/mni/cond/cone/smoothed/cone_group_z.nii.gz \
#-o /scratch/09123/ofriend/moshi/grid_coding/mni/cond/cone/smoothed/age_grouped \
#-d /scratch/09123/ofriend/moshi/grid_coding/randomise/new/age_grouped_cone.mat \
#-t /scratch/09123/ofriend/moshi/grid_coding/randomise/new/age_grouped_cone.con \
#-m /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/mni_gm_2mm_dil_masked.nii.gz \
#-n 5000 -x --uncorrp


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