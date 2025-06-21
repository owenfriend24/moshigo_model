#!/usr/bin/env python

import os
import sys
import subprocess
import pandas as pd
from nilearn.image import load_img
from nilearn.glm.first_level import FirstLevelModel

# ========== USER INPUT ==========
fmriprep_dir = "/scratch/09123/ofriend/moshi/grid_coding/"
expdir = "/corral-repl/utexas/prestonlab/moshiGO1"
runs = [1, 2, 3, 4, 5, 6]
TR = 2.0

subject = sys.argv[1]
print(f"Processing {subject}")

subj_exp_dir = os.path.join(expdir, subject)
subj_scratch_dir = os.path.join(fmriprep_dir, subject)
acf_outdir = os.path.join(fmriprep_dir, "acf")
os.makedirs(acf_outdir, exist_ok=True)
subject_output_csv = os.path.join(acf_outdir, f"{subject}_acf.csv")

# ========== LOAD MODULE IF NEEDED ==========
subprocess.run("module load afni", shell=True)

results = []

for run in runs:
    print(f"Run {run}")
    bold_path = f"{subj_exp_dir}/BOLD/antsreg/data/task_run{run}_bold_mcf_brain.nii.gz"
    motion_path = f"{subj_exp_dir}/BOLD/task_run{run}/QA/confound.txt"
    gm_path = f'{subj_exp_dir}/anatomy/antsreg/data/funcunwarpspace/rois/freesurfer/b_gray_dilated.nii.gz'
    fitted_path = f"{subj_scratch_dir}/acf_outputs/{subject}_run-{run}_motion_model.nii.gz"
    temp_mask_path = f"{subj_scratch_dir}/acf_outputs/tmp_b_gray_mask_run{run}.nii.gz"
    os.makedirs(os.path.dirname(fitted_path), exist_ok=True)

    if not (os.path.exists(bold_path) and os.path.exists(motion_path) and os.path.exists(gm_path)):
        print(f"Missing data for {subject}, run {run}, skipping.")
        continue

    try:
        # Save gray matter mask as temp file
        gm_img = load_img(gm_path)
        gm_img.to_filename(temp_mask_path)

        # Load and fit motion-only model
        func_img = load_img(bold_path)
        motion_df = pd.read_csv(motion_path, delim_whitespace=True, header=None)

        model = FirstLevelModel(t_r=TR, noise_model="ols", standardize=False, minimize_memory=False)
        model = model.fit(func_img, design_matrices=motion_df)
        fitted_img = model.predicted[0]
        fitted_img.to_filename(fitted_path)

        def run_3dfwhmx(img_path, mask_path):
            cmd = [
                "3dFWHMx",
                "-mask", mask_path,
                "-ACF", "NULL",
                "-input", img_path,
                "-arith"
            ]
            output = subprocess.check_output(cmd, universal_newlines=True)
            return list(map(float, output.strip().split("\n")[-1].strip().split()[-4:]))

        # Get ACF for motion model
        a_m, b_m, c_m, d_m = run_3dfwhmx(fitted_path, temp_mask_path)
        # Get ACF for raw image
        a_r, b_r, c_r, d_r = run_3dfwhmx(bold_path, temp_mask_path)

        results.append({
            "subject": subject,
            "run": run,
            "a_motion": a_m, "b_motion": b_m, "c_motion": c_m, "d_motion": d_m,
            "a_raw": a_r, "b_raw": b_r, "c_raw": c_r, "d_raw": d_r
        })
        print(f"     ✅ Motion a={a_m:.3f}, Raw a={a_r:.3f}")

    except Exception as e:
        print(f"Error for {subject} run {run}: {e}")

    finally:
        if os.path.exists(temp_mask_path):
            os.remove(temp_mask_path)

# ========== SAVE PER-SUBJECT OUTPUT ==========
df = pd.DataFrame(results)
df.to_csv(subject_output_csv, index=False)
print(f"\nACF values saved to: {subject_output_csv}")
