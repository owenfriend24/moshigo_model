#!/bin/env bash
#
# cluster simulations for preliminary age group RS analyses

if [[ $# -lt 1 ]]; then
    echo "Usage: clust_sim.sh fmriprep_dir"
    exit 1
fi

fmriprep_dir=$1

module load afni
export OMP_NUM_THREADS=None

mkdir -p /scratch/09123/ofriend/moshi/grid_coding/clust_sim
cd /scratch/09123/ofriend/moshi/grid_coding/clust_sim

#3dClustSim -mask /scratch/09123/ofriend/moshi/grid_coding/mni/erc/masks/group_mask_025.nii.gz -acf 0.793816 1.126296 8.651422 -nodec -prefix erc_new
#3dClustSim -mask /scratch/09123/ofriend/moshi/grid_coding/mni/mni_masks/func_masks/b_erc.nii.gz -acf 0.793816 1.126296 8.651422 -nodec -prefix b_erc_motion_
#3dClustSim -mask /scratch/09123/ofriend/moshi/grid_coding/mni/mni_masks/func_masks/b_Olsen_alERC.nii.gz -acf 0.793816 1.126296 8.651422 -nodec -prefix al_erc_motion_
#3dClustSim -mask /scratch/09123/ofriend/moshi/grid_coding/mni/mni_masks/func_masks/b_Olsen_pmERC.nii.gz -acf 0.793816 1.126296 8.651422 -nodec -prefix pm_erc_motion_

3dClustSim -mask /home1/09123/ofriend/analysis/moshigo_model/mni_gm_2mm.nii.gz -acf 0.792 1.130 8.685 -nodec -prefix FINAL_GM

3dClustSim -mask /scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/mni_gm_2mm_dil_masked.nii.gz -acf 0.792 1.130 8.685 -nodec -prefix FINAL_GM_DIL

#3dClustSim -mask /scratch/09123/ofriend/moshi/grid_coding/mni/mni_masks/func_masks/b_erc.nii.gz -acf 0.382950 2.805128 10.545258 -nodec -prefix b_erc_
#3dClustSim -mask /scratch/09123/ofriend/moshi/grid_coding/mni/mni_masks/func_masks/b_Olsen_pmERC.nii.gz -acf 0.382950 2.805128 10.545258 -nodec -prefix pm_erc_
