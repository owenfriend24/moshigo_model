#!/usr/bin/env python

import subprocess
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
import argparse

subprocess.run(['/bin/bash', '-c', 'source /home1/09123/ofriend/analysis/temple/rsa/bin/activate'])

# custom grid function
from grid_function_modulo60 import *

def get_args():
    parser = argparse.ArgumentParser(description="Process fMRI data for pre/post comparison.")
    parser.add_argument("subject_id", help="Subject identifier (e.g., temple016)")
    # optional argument: drop a specific run
    parser.add_argument("condition", type=str, choices=["both", "mountain", "cone"], default="both",
                        help="both, mountain, or cone")
    parser.add_argument("mask", type=str, choices=["gm", "erc"], default="gm",
                        help="gm or erc")
    parser.add_argument("--drop_run", type=int, choices=[1, 2, 3, 4, 5, 6], default=None,
                        help="Run number to drop (1 through 6). Default is None (keep all runs).")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    sbj = args.subject_id

    condition = args.condition
    drop_run = args.drop_run
    mask = args.mask

    # run within specific conditions if necessary
    if condition == 'cone':
        cond_flag = '_cone'
    elif condition == 'mountain':
        cond_flag = '_mountain'
    else:
        cond_flag = ''

    func_data = f'grid_trials{cond_flag}.nii.gz'

    expdir = f'/scratch/09123/ofriend/moshi/grid_coding'
    subjdir = f'{expdir}/{sbj}/'
    funcdir = f'/{subjdir}/grid_data/'
    out_dir = funcdir
    niter= 1000


    # load metadata
    if condition == 'both':
        meta = pd.read_csv(f'/scratch/09123/ofriend/moshi/grid_coding/{sbj}/grid_data/all_runs_meta.txt',
                           sep='\t', header=None, names=["run", "img", "trial_angle"])
    elif condition == 'cone':
        meta = pd.read_csv(f'/scratch/09123/ofriend/moshi/grid_coding/{sbj}/grid_data/all_runs_meta_cone.txt',
                           sep='\t', header=None, names=["run", "img", "trial_angle"])
    elif condition == 'mountain':
        meta = pd.read_csv(f'/scratch/09123/ofriend/moshi/grid_coding/{sbj}/grid_data/all_runs_meta_mountain.txt',
                           sep='\t', header=None, names=["run", "img", "trial_angle"])

    run = meta["run"].to_numpy()
    trial_angle = meta["trial_angle"].to_numpy()
    img = meta["img"].to_numpy()

    if mask == 'gm':
        masks = ['b_gray_dilated']
    elif mask == 'erc':
        masks = ['erc']

    # mask to run searchlight in
    for mask in masks:
        if mask in ['b_gray_dilated']:
            slmask = f'/corral-repl/utexas/prestonlab/moshiGO1/{sbj}/anatomy/antsreg/data/funcunwarpspace/rois/freesurfer/{mask}.nii.gz'
        else:
            slmask = f'/scratch/09123/ofriend/moshi/erc_masks/b_masks/func/{sbj}_b_{mask}.nii.gz'
        ds = fmri_dataset(os.path.join(funcdir, func_data), mask=slmask)
        ds.sa['run'] = run
        ds.sa['trial_angle'] = trial_angle

        # run across all runs
        sl_func = grid_function_modulo60('correlation', niter=niter)
        sl = sphere_searchlight(sl_func, radius=3)
        sl_result = sl(ds)
        sl_map_60_ovr_30 = sl_result
        outfile_60 = f'{out_dir}/{sbj}_60_ovr_30_{mask}{cond_flag}_z.nii.gz'
        map2nifti(ds, sl_map_60_ovr_30.samples).to_filename(outfile_60)


    subprocess.run(["bash", "/home1/09123/ofriend/analysis/moshigo_model/bin/transform_sl_to_2mm.sh", sbj])