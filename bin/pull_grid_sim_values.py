#!/usr/bin/env python
import subprocess

subprocess.run(['/bin/bash', '-c', 'source /home1/09123/ofriend/analysis/temple/rsa/bin/activate'])
### import python libraries needed for the analysis ###
import numpy as np
import pandas as pd
import nibabel
import scipy.stats
from scipy.stats.mstats import zscore
from scipy.ndimage import convolve1d
from scipy.sparse import spdiags
from scipy.linalg import toeplitz
from mvpa2.datasets.mri import *
import os
import sys
from random import sample
from mvpa2.datasets.mri import *
from mvpa2.mappers.detrend import *
from mvpa2.mappers.zscore import *
from mvpa2.clfs.svm import *
from mvpa2.generators.partition import *
from mvpa2.measures.base import *
from mvpa2.measures import *
from mvpa2.measures.searchlight import *
from mvpa2.misc.stats import *
from mvpa2.base.node import *
from mvpa2.clfs.meta import *
from mvpa2.clfs.stats import *
from mvpa2.featsel.base import *
from mvpa2.featsel.helpers import *
from mvpa2.generators.permutation import *
from mvpa2.generators.base import *
from mvpa2.mappers.fx import *
from mvpa2.measures.anova import *
from mvpa2.base.dataset import *
import sys
import subprocess
import argparse

### import custom searchlight function ###
from grid_similarity_function import *

### use argument parser to set up experiment/subject info and drop runs if necessary
def get_args():
    parser = argparse.ArgumentParser(description="Process fMRI data for pre/post comparison.")
    # Required arguments
    parser.add_argument("subject_id", help="Subject identifier (e.g., temple016)")
    # Optional argument: drop a specific run
    parser.add_argument("--drop_run", type=int, choices=[1, 2, 3, 4, 5, 6], default=None,
                        help="Run number to drop (1 through 6). Default is None (keep all runs).")

    return parser.parse_args()

def back_project_to_func_space(sbj, masks):
    for mask in masks:
        if sbj in ["moshiGO_250", "moshiGO_230", "moshiGO_285", "moshiGO_334", "moshiGO_277", "moshiGO_240", "moshiGO_247", "moshiGO_213", "moshiGO_350", "moshiGO_323"]:
            warp = f"/corral-repl/utexas/prestonlab/temple/moshigo/results/{sbj}/test_new_func_to_mni1mm_Warp.nii.gz"
            affine  = f"/corral-repl/utexas/prestonlab/temple/moshigo/results/{sbj}/test_new_func_to_mni1mm_Affine.txt"
        else:
            warp = f"/corral-repl/utexas/prestonlab/moshiGO1/{sbj}/anatomy/antsreg/transforms/brain2MNI_1mm_Warp.nii.gz"
            affine = f"/corral-repl/utexas/prestonlab/moshiGO1/{sbj}/anatomy/antsreg/transforms/brain2MNI_1mm_Affine.txt"

        input_mask = f"/scratch/09123/ofriend/moshi/grid_coding/mni/mni_masks/func_masks/{mask}.nii.gz"
        output_mask = f'/scratch/09123/ofriend/moshi/grid_coding/{sbj}/1mm_{mask}_mni.nii.gz'
        reference = f'/home1/09123/ofriend/analysis/temple/bin/templates/MNI152_T1_1mm_brain.nii.gz'
        cmd1 = [
            "antsApplyTransforms",
            "-d", "3",
            "-i", input_mask,
            "-o", output_mask,
            "-r", reference,
            "-n", "NearestNeighbor"
        ]

        input_mask = f'/scratch/09123/ofriend/moshi/grid_coding/{sbj}/1mm_{mask}_mni.nii.gz'
        output_mask = f'/scratch/09123/ofriend/moshi/grid_coding/{sbj}/func_{mask}.nii.gz'
        reference = f'/scratch/09123/ofriend/moshi/grid_coding/{sbj}/grid_data/grid_trials.nii.gz'
        cmd2 = [
            "antsApplyTransforms",
            "-d", "3",
            "-i", input_mask,
            "-o", output_mask,
            "-r", reference,
            "-t", warp,
            "-t", f"[{affine},1]",
            "-n", "NearestNeighbor"
        ]

        subprocess.run(cmd1, check=True)
        subprocess.run(cmd2, check=True)


### Main script execution ###
if __name__ == "__main__":
    args = get_args()
    sbj = args.subject_id
    drop_run = args.drop_run

    expdir = f'/scratch/09123/ofriend/moshi/grid_coding'
    subjdir = f'{expdir}/{sbj}/'
    funcdir = f'/{subjdir}/grid_data/'
    out_dir = funcdir

    masks = ['mpfc_age_inc', 'pm_erc_age_dec', 'pm_erc_age_dec_masked']
    back_project_to_func_space(sbj, masks)

    meta = pd.read_csv(f'/scratch/09123/ofriend/moshi/grid_coding/{sbj}/grid_data/all_runs_meta.txt',
                       sep='\t', header=None, names=["run", "img", "trial_angle"])

    run = meta["run"].to_numpy()
    trial_angle = meta["trial_angle"].to_numpy()
    img = meta["img"].to_numpy()

    for mask in masks:
        slmask = f'/scratch/09123/ofriend/moshi/grid_coding/{sbj}/func_{mask}.nii.gz'
        ds = fmri_dataset(os.path.join(funcdir, 'grid_trials.nii.gz'), mask=slmask)

        # REMOVE voxels with any NaNs
        good_voxels = ~np.any(np.isnan(ds.samples), axis=0)
        if not np.all(good_voxels):
            print(f"{sbj} {mask}: Removed {np.sum(~good_voxels)} voxels with NaNs")
        ds = ds[:, good_voxels]  # Keep all trials, drop bad voxels

        ds.sa['run'] = run
        ds.sa['trial_angle'] = trial_angle

        sl_func = grid_similarity_function('correlation')
        result_df = sl_func(ds)

        out_path = f'{subjdir}/{mask}_similarity_values.csv'
        result_df.to_csv(out_path, index=False)

