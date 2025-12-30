#!/usr/bin/env python


import subprocess
from sklearn.decomposition import PCA
import numpy as np
import nibabel
import scipy.stats
from scipy.stats.mstats import zscore
from scipy.ndimage import convolve1d
from scipy.sparse import spdiags
from scipy.linalg import toeplitz
from mvpa2.datasets.mri import *
import os
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


# import custom searchlight function using adapted pymvpa package
from searchlight_function_pca import *


def get_args():
    parser = argparse.ArgumentParser(description="Process fMRI data for pre/post comparison.")
    # required arguments
    parser.add_argument("subject_id", help="Subject identifier (e.g., temple016)")
    parser.add_argument("masktype", help="Mask type (e.g., whole_brain)")
    # optional argument: drop a specific run
    parser.add_argument("--drop_run", type=int, choices=[1, 2, 3, 4, 5, 6], default=None,
                        help="Run number to drop (1 through 6). Default is None (keep all runs).")

    return parser.parse_args()

# execute main searchlight
if __name__ == "__main__":
    args = get_args()
    sbj = args.subject_id
    masktype = args.masktype
    drop_run = args.drop_run

    expdir = '/corral-repl/utexas/prestonlab/moshiGO1/'
    subjdir = os.path.join(expdir, f'{sbj}')
    betadir = f'{expdir}/{sbj}/RSAmodel/betaseries/'
    resultdir = f'/scratch/09123/ofriend/moshi/pca_sl/results/'
    out_dir = os.path.join(resultdir, f'{sbj}')
    os.makedirs(out_dir, exist_ok=True)
    niter= 1000

    if masktype == 'gm':
        masks = ['b_gray']
    elif masktype == 'brain_mask':
        masks = ['brain_mask']

    run, item = np.loadtxt(
        f'/home1/09123/ofriend/analysis/moshigo_model/bin/all_items.txt',
        unpack=True
    )

    for mask in masks:
        if masktype == 'gm':
            slmask = f'{expdir}/{sbj}/anatomy/antsreg/data/funcunwarpspace/rois/freesurfer/{mask}_dilated.nii.gz'
        elif masktype == 'brain_mask':
            slmask = f'{expdir}/{sbj}/anatomy/antsreg/data/funcunwarpspace/{mask}.nii.gz'

        #load in data
        ds = fmri_dataset(os.path.join(betadir, 'moshiGO_allruns.gz'), mask=slmask)

        ds.sa['run'] = run[:]
        ds.sa['item'] = item[:]

        # make sure to drop runs for subjects that didn't complete full task
        for run_id in range (1, 7, 1):
            ds_run = ds[ds.sa.run == run_id]

            # run the searchlight for variance explained by top 2 PC's
            sl_result = sphere_searchlight(searchlight_function_pca(n_components=4), radius=3)(ds_run)
            sl_img = map2nifti(ds_run, sl_result)
            sl_img.to_filename(f"{out_dir}/{sbj}_run-{run_id}_pca12_varExpl_{mask}.nii.gz")