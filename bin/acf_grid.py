#!/usr/bin/env python

import os
import subprocess
import pandas as pd
from nilearn.image import load_img
from nilearn.glm.first_level import FirstLevelModel

# ========== USER INPUT ==========
fmriprep_dir = "/scratch/09123/ofriend/moshi/grid_coding/"
expdir = "/corral-repl/utexas/prestonlab/moshiGO1"
subject_list = ["moshiGO_201", "moshiGO_202", "moshiGO_203", "moshiGO_208", "moshiGO_211", "moshiGO_212", "moshiGO_213", "moshiGO_220", "moshiGO_221", "moshiGO_222", "moshiGO_223", "moshiGO_224", "moshiGO_226", "moshiGO_228", "moshiGO_229", "moshiGO_230", "moshiGO_231", "moshiGO_232", "moshiGO_235", "moshiGO_238", "moshiGO_239", "moshiGO_240", "moshiGO_241", "moshiGO_243", "moshiGO_246", "moshiGO_247", "moshiGO_248", "moshiGO_249", "moshiGO_250", "moshiGO_251", "moshiGO_252", "moshiGO_253", "moshiGO_255", "moshiGO_258", "moshiGO_259", "moshiGO_260", "moshiGO_261", "moshiGO_262", "moshiGO_266", "moshiGO_268", "moshiGO_270", "moshiGO_271", "moshiGO_273", "moshiGO_277", "moshiGO_278", "moshiGO_279", "moshiGO_280", "moshiGO_281", "moshiGO_282", "moshiGO_284", "moshiGO_285", "moshiGO_289", "moshiGO_291", "moshiGO_292", "moshiGO_293", "moshiGO_294", "moshiGO_297", "moshiGO_298", "moshiGO_302", "moshiGO_304", "moshiGO_305", "moshiGO_306", "moshiGO_308", "moshiGO_310", "moshiGO_312", "moshiGO_313", "moshiGO_314", "moshiGO_315", "moshiGO_316", "moshiGO_320", "moshiGO_321", "moshiGO_322", "moshiGO_323", "moshiGO_324", "moshiGO_327", "moshiGO_329", "moshiGO_331", "moshiGO_333", "moshiGO_334", "moshiGO_336", "moshiGO_339", "moshiGO_341", "moshiGO_343", "moshiGO_345", "moshiGO_350", "moshiGO_351"]
runs = [1, 2, 3, 4, 5, 6]
TR = 2.0
output_csv = os.path.join(fmriprep_dir, "acf", "acf_motion_vs_raw.csv")
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

results = []

for subject in subject_list:
    print(f"Processing {subject}...")
    subj_exp_dir = os.path.join(expdir, subject)
    subj_scratch_dir = os.path.join(fmriprep_dir, subject)
    for run in runs:
        print(f"running for run {run}")
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

            model = FirstLevelModel(t_r=TR, noise_model="ols", standardize=False)
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
            print(f"Motion a={a_m:.3f}, Raw a={a_r:.3f}")

        except Exception as e:
            print(f"Error for {subject} run {run}: {e}")
        finally:
            # Cleanup temp mask file
            if os.path.exists(temp_mask_path):
                os.remove(temp_mask_path)

df = pd.DataFrame(results)
df.to_csv(output_csv, index=False)
print(f"ACF values saved to: {output_csv}")
