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

def combine_lateral_masks(sbj):
    base = "/scratch/09123/ofriend/moshi/erc_masks/"

    if os.path.exists(f"{base}/{sbj}_R_ERC.nii.gz"):
        r = f"{base}/{sbj}_R_ERC.nii.gz"
    else:
        r = f"{base}/{sbj}_olsen_R_ERC.nii.gz"

    if os.path.exists(f"{base}/{sbj}_L_ERC.nii.gz"):
        l = f"{base}/{sbj}_L_ERC.nii.gz"
    else:
        l = f"{base}/{sbj}_olsen_L_ERC.nii.gz"

    out_dir = f"{base}/b_masks"
    out_path = f"{out_dir}/{sbj}_b_erc.nii.gz"
    cmd_merge = ["fslmaths", r, "-add", l, out_path]
    subprocess.run(cmd_merge, check=True)

def coronal_to_func(sbj):
    base = "/scratch/09123/ofriend/moshi/erc_masks/"
    input_mask =  f"{base}/b_masks/{sbj}_b_erc.nii.gz"
    output_mask = f"{base}/b_masks/func/{sbj}_b_erc.nii.gz"
    reference = f'/corral-repl/utexas/prestonlab/moshiGO1/{sbj}/anatomy/antsreg/data/funcunwarpspace/brain.nii.gz'
    warp = f"/corral-repl/utexas/prestonlab/temple/moshigo/results/{sbj}/NEW_coronal_to_func_Warp.nii.gz"
    affine = f"/corral-repl/utexas/prestonlab/temple/moshigo/results/{sbj}/NEW_coronal_to_func_Affine.txt"
    cmd_cor = [
        "antsApplyTransforms",
        "-d", "3",
        "-i", input_mask,
        "-o", output_mask,
        "-n", "Linear",
        "-r", reference
      #  "-t", warp,
       # "-t", f"[{affine},1]",
        #"-n", "NearestNeighbor"
    ]
    subprocess.run(cmd_cor, check=True)
    cmd_binarize = [
        "fslmaths",
        output_mask,
        "-bin",
        output_mask
    ]
    subprocess.run(cmd_binarize, check=True)

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

        input_mask = f"/scratch/09123/ofriend/moshi/grid_coding/mni/new2/smoothed/masked/{mask}.nii.gz"
        #input_mask = f"/scratch/09123/ofriend/moshi/grid_coding/mni/mni_masks/func_masks/{mask}.nii.gz"

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
    maskdir = f'/scratch/09123/ofriend/moshi/erc_masks/b_masks/'
    subjdir = f'{expdir}/{sbj}/'
    funcdir = f'{subjdir}/grid_data/'
    out_dir = funcdir

    #masks = ['perf_ifg', 'perf_precuneus', 'perf_parietal', 'perf_phc']

    #back_project_to_func_space(sbj, masks)
    #combine_lateral_masks(sbj)
    #coronal_to_func(sbj)

    # Load trial metadata; can come back and restrict by condition


    meta = pd.read_csv(f'{funcdir}/all_runs_meta_cone.txt',
                       sep='\t', header=None, names=["run", "img", "trial_angle"])

    run = meta["run"].to_numpy()
    trial_angle = meta["trial_angle"].to_numpy()
    img = meta["img"].to_numpy()

    all_results = []
    masks = ['erc']
    for mask in masks:
        slmask = f'{maskdir}/func/{sbj}_b_erc.nii.gz'

        ds = fmri_dataset(os.path.join(funcdir, 'grid_trials_cone.nii.gz'), mask=slmask)

        #ds = fmri_dataset(os.path.join(funcdir, 'grid_trials.nii.gz'), mask=slmask)

        ds.sa['run'] = run
        ds.sa['trial_angle'] = trial_angle

        sl_func = grid_similarity_function('correlation')
        result_df = sl_func(ds)

        # Add subject and ROI info to result
        result_df['subject'] = sbj
        result_df['roi'] = mask

        all_results.append(result_df)


    combined_df = pd.concat(all_results, ignore_index=True)
    master_csv_path = f'{expdir}/csvs/sub_roi_similarity_values.csv'
    write_header = not os.path.exists(master_csv_path)

    # Append subject to master csv
    combined_df.to_csv(master_csv_path, mode='a', header=write_header, index=False)







