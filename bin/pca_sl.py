#!/usr/bin/env python
import subprocess
from sklearn.decomposition import PCA

subprocess.run(['/bin/bash', '-c', 'source /home1/09123/ofriend/analysis/temple/rsa/bin/activate'])
### import python libraries needed for the analysis ###
import numpy as np
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
from searchlight_function_pca import *


### use argument parser to set up experiment/subject info and drop runs if necessary
def get_args():
    parser = argparse.ArgumentParser(description="Process fMRI data for pre/post comparison.")

    # Required arguments
    parser.add_argument("subject_id", help="Subject identifier (e.g., temple016)")
    parser.add_argument("masktype", help="Mask type (e.g., whole_brain)")
    # Optional argument: drop a specific run
    parser.add_argument("--drop_run", type=int, choices=[1, 2, 3, 4, 5, 6], default=None,
                        help="Run number to drop (1 through 6). Default is None (keep all runs).")

    return parser.parse_args()


### Main script execution ###
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
    #expdir = '/scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep'
    niter= 1000

    ### masks for data to analyze ###
    if masktype == 'gm':
        masks = ['b_gray']
    elif masktype == 'brain_mask':
        masks = ['brain_mask']

    run, item = np.loadtxt(
        f'/home1/09123/ofriend/analysis/moshigo_model/bin/phase_1_items.txt',
        unpack=True
    )


    ###
    for mask in masks:
        if masktype == 'gm':
            slmask = f'{expdir}/{sbj}/anatomy/antsreg/data/funcunwarpspace/rois/freesurfer/{mask}_dilated.nii.gz'
        elif masktype == 'brain_mask':
            slmask = f'{expdir}/{sbj}/anatomy/antsreg/data/funcunwarpspace/{mask}.nii.gz'

        #load in data
        ds = fmri_dataset(os.path.join(betadir, 'phase_1.nii.gz'), mask=slmask)

        ds.sa['run'] = run[:]
        ds.sa['item'] = item[:]

# choose the function based on the comparison as some sl logic changes by comparison

        for run_id in [1, 2, 3]:
            ds_run = ds[ds.sa.run == run_id]

            #run the searchlight
            sl_result = sphere_searchlight(searchlight_function_pca(n_components=4), radius=3)(ds_run)
            sl_img = map2nifti(ds_run, sl_result)
            sl_img.to_filename(f"{out_dir}/{sbj}_run-{run_id}_pca12_varExpl_{mask}.nii.gz")
