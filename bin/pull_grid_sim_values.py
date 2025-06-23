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
    ref_func = f'/scratch/09123/ofriend/moshi/grid_coding/{sbj}/grid_data/grid_ref.nii.gz'
    cmd0 = [
        "fslmaths",
        f'/scratch/09123/ofriend/moshi/grid_coding/{sbj}/grid_data/grid_trials.nii.gz',
        "-Tmean",
        ref_func
    ]
    subprocess.run(cmd0, check=True)

    for mask in masks: # 222 looks off
        warp = f"/corral-repl/utexas/prestonlab/temple/moshigo/results/{sbj}/NEW_func_to_mni2mm_InverseWarp.nii.gz"
        affine = f"/corral-repl/utexas/prestonlab/temple/moshigo/results/{sbj}/NEW_func_to_mni2mm_Affine.txt"

        # input_mask = f"/scratch/09123/ofriend/moshi/grid_coding/mni/new/smoothed/{mask}.nii.gz"
        # output_mask = f'/scratch/09123/ofriend/moshi/grid_coding/{sbj}/1mm_{mask}_mni.nii.gz'
        # reference = f'/home1/09123/ofriend/analysis/temple/bin/templates/MNI152_T1_1mm_brain.nii.gz'
        # cmd1 = [
        #     "antsApplyTransforms",
        #     "-d", "3",
        #     "-i", input_mask,
        #     "-o", output_mask,
        #     "-r", reference,
        #     "-n", "NearestNeighbor"
        # ]

        #input_mask = f"/scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/{mask}.nii.gz"
        input_mask = f"/scratch/09123/ofriend/moshi/grid_coding/mni/mni_masks/func_masks/{mask}.nii.gz"

        output_mask = f'/scratch/09123/ofriend/moshi/grid_coding/{sbj}/NEW_func_{mask}.nii.gz'
        reference = f'/corral-repl/utexas/prestonlab/moshiGO1/{sbj}/anatomy/antsreg/data/funcunwarpspace/brain.nii.gz'

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
        ref_mask = f'/scratch/09123/ofriend/moshi/grid_coding/{sbj}/brain_mask.nii.gz'
        cmd3 = [
            "fslmaths",
            reference,
            "-bin",
            ref_mask
        ]
        cmd4 = [
            "fslmaths",
            output_mask,
            "-mas",
            ref_mask,
            output_mask
        ]

        # subprocess.run(cmd1, check=True)
        subprocess.run(cmd2, check=True)
        subprocess.run(cmd3, check=True)
        subprocess.run(cmd4, check=True)
        # # # clean mask to make sure no missing voxels
        # brain_mask = f"/corral-repl/utexas/prestonlab/moshiGO1/{sbj}/anatomy/antsreg/data/funcunwarpspace/brain_mask.nii.gz"
        # cmd3 = [
        #     "fslmaths",
        #     f'/scratch/09123/ofriend/moshi/grid_coding/{sbj}/func_{mask}_pre.nii.gz',
        #     "-mas",
        #     brain_mask,
        #     f'/scratch/09123/ofriend/moshi/grid_coding/{sbj}/func_{mask}.nii.gz'
        # ]
        # subprocess.run(cmd3, check=True)

### Main script execution ###
if __name__ == "__main__":
    args = get_args()
    sbj = args.subject_id
    drop_run = args.drop_run

    expdir = f'/scratch/09123/ofriend/moshi/grid_coding'
    subjdir = f'{expdir}/{sbj}/'
    funcdir = f'/{subjdir}/grid_data/'
    out_dir = funcdir

    #masks = ['precuneus', 'precuneus2', 'phc', 'dmpfc', 'mpfc1', 'mpfc2']
    masks = ['AD_Barron_LERC', 'AD_Barron_RERC', 'AD_Olsen_LalERC', 'AD_Olsen_LERC', 'AD_Olsen_LpmERC', 'AD_Olsen_RalERC', 'AD_Olsen_RERC', 'AD_Olsen_RpmERC', 'b_Barron_ERC', 'b_erc', 'b_Olsen_alERC', 'b_Olsen_ERC', 'b_Olsen_pmERC', 'l_erc', 'r_erc']
    back_project_to_func_space(sbj, masks)

    meta = pd.read_csv(f'/scratch/09123/ofriend/moshi/grid_coding/{sbj}/grid_data/all_runs_meta.txt',
                       sep='\t', header=None, names=["run", "img", "trial_angle"])

    run = meta["run"].to_numpy()
    trial_angle = meta["trial_angle"].to_numpy()
    img = meta["img"].to_numpy()

    for mask in masks:
        slmask = f'/scratch/09123/ofriend/moshi/grid_coding/{sbj}/NEW_func_{mask}.nii.gz'
        ds = fmri_dataset(os.path.join(funcdir, 'grid_trials.nii.gz'), mask=slmask)


        ds.sa['run'] = run
        ds.sa['trial_angle'] = trial_angle

        sl_func = grid_similarity_function('correlation')
        result_df = sl_func(ds)

        out_path = f'/scratch/09123/ofriend/moshi/grid_coding/csvs/{sbj}_{mask}_similarity_values.csv'
        result_df.to_csv(out_path, index=False)