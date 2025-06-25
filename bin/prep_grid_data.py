#!/usr/bin/env python

import os
import argparse
import subprocess
import numpy as np
import pandas as pd
from nilearn.glm.first_level import FirstLevelModel
from nilearn.image import load_img, index_img, new_img_like
from nilearn.masking import apply_mask, unmask

# Activate virtual environment (if needed)
subprocess.run(['/bin/bash', '-c', 'source /home1/09123/ofriend/analysis/temple/rsa/bin/activate'])

def get_args():
    parser = argparse.ArgumentParser(description="Process fMRI data for grid analysis.")
    parser.add_argument("subject_id", help="Subject identifier (e.g., moshiGO_202)")
    parser.add_argument("condition", type=str, choices=["both", "cone", "mountain"], default="both",
                        help="Run number to drop (1–6). Default: keep all runs.")
    parser.add_argument("--drop_run", type=int, choices=[1, 2, 3, 4, 5, 6], default=None,
                        help="Run number to drop (1–6). Default: keep all runs.")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    sub = args.subject_id
    drop_run = args.drop_run
    condition = args.condition

    # Define paths
    expdir = '/corral-repl/utexas/prestonlab/moshiGO1'
    subjdir = f'{expdir}/{sub}'
    outdir = f'/scratch/09123/ofriend/moshi/grid_coding/{sub}/grid_data/'
    os.makedirs(outdir, exist_ok=True)
    TR = 2.0

    behav_master = pd.read_csv("/home1/09123/ofriend/analysis/moshigo_model/onsets_and_grid_angles.csv")
    sub_id = sub[-3:]
    trial_data = behav_master[behav_master['subject'] == int(sub_id)].copy().reset_index(drop=True)

    # Load gray matter mask
    gm_path = f'{subjdir}/anatomy/antsreg/data/funcunwarpspace/rois/freesurfer/b_gray_dilated.nii.gz'
    gray_matter_mask = load_img(gm_path)

    # Store metadata across runs
    all_metas = []
    run_range = 7
    if sub in ['moshiGO_289','moshiGO_230','moshiGO_285','moshiGO_294','moshiGO_345','moshiGO_241','moshiGO_277','moshiGO_316',
               'moshiGO_248','moshiGO_213','moshiGO_278','moshiGO_334','moshiGO_321','moshiGO_255']:
        run_range = 4
    for run in range(1, run_range):
        print(f"processing run {run}")
        if drop_run is not None and run == drop_run:
            print(f"Skipping run {run}")
            continue

        print(f"Processing run {run}...")
        run_data = trial_data[trial_data['run'] == run].copy()
        if run_data.empty:
            print(f"No trials found for run {run}, skipping.")
            continue

        if condition == 'cone':
            run_data = run_data[run_data['condition'] < 3]
        elif condition == 'mountain':
            run_data = run_data[run_data['condition'] > 2]

        # Load functional data and confounds
        func_path = f'{subjdir}/BOLD/antsreg/data/task_run{run}_bold_mcf_brain.nii.gz'
        func_img = load_img(func_path)

        motion_path = f'{subjdir}/BOLD/task_run{run}/QA/confound.txt'
        motion_df = pd.read_csv(motion_path, delim_whitespace=True, header=None)
        motion_confounds = motion_df
        n_scans = func_img.shape[-1]

        # Fit GLM and get residuals
        model = FirstLevelModel(t_r=TR, noise_model='ols', standardize=False, minimize_memory=False)
        model = model.fit(func_img, design_matrices=motion_confounds)
        residuals_img = model.residuals[0]
        print("created residuals image")

        # Convert movement start time to TR indices
        onset_TRs = (np.array(run_data['mvmt_start']) / TR).astype(int)
        TR_indices = [list(range(t, t + 3)) for t in onset_TRs]
        run_data["TR_indices"] = TR_indices

        # Mask residuals once
        masked_data = apply_mask(residuals_img, gray_matter_mask)
        print("masked residuals to gray matter")

        # Compute trial-wise averaged patterns
        trial_patterns = []
        kept_indices = []

        for idx, row in run_data.iterrows():
            tr_window = [tr for tr in row["TR_indices"] if tr < masked_data.shape[0]]
            if not tr_window:
                print(f"no valid TRs in window {idx + 1} run {run}")
                continue
            pattern = masked_data[tr_window].mean(axis=0)
            trial_patterns.append(pattern)
            kept_indices.append(idx)

        # Align run_data to match kept trials
        run_data = run_data.loc[kept_indices].reset_index(drop=True)
        trial_patterns = np.vstack(trial_patterns)
        print("extracted navigation TRs")

        # Save each trial as a NIfTI file and record metadata
        img_names = []
        for i, pattern in enumerate(trial_patterns):
            trial_img = unmask(pattern, gray_matter_mask)
            img_name = f"trial_run{run}_{i + 1:03d}.nii.gz"
            trial_img.to_filename(os.path.join(outdir, img_name))
            img_names.append(img_name)

        grid_meta = pd.DataFrame({
            'run': run_data['run'].astype(int),
            'img_name': img_names,
            'trial_angle': run_data['trial_angle']
        })

        grid_meta.to_csv(f'{outdir}/run{run}_meta.txt', sep='\t', index=False, header=False)
        all_metas.append(grid_meta)

    # Save full combined metadata
    combined_meta = pd.concat(all_metas).reset_index(drop=True)
    combined_meta.to_csv(f'{outdir}/all_runs_meta.txt', sep='\t', index=False, header=False)
    print(f"Saved combined metadata to {outdir}/all_runs_meta.txt")

    # combine all trials into a single 4d image
    merged_img_path = os.path.join(outdir, "grid_trials.nii.gz")
    img_list = [os.path.join(outdir, fname) for fname in combined_meta["img_name"]]
    fslmerge_cmd = ["fslmerge", "-t", merged_img_path] + img_list
    print("Merging trial images with fslmerge...")
    subprocess.run(fslmerge_cmd, check=True)
    print(f"Saved merged 4D image to {merged_img_path}")

