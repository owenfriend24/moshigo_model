#!/usr/bin/env python

import nibabel as nib
import numpy as np
import pandas as pd
import os
import sys

def extract_mean_roi_zvals(run_type):
    expdir = '/scratch/09123/ofriend/moshi/grid_coding/'
    csv_path = f'/scratch/09123/ofriend/moshi/grid_coding/grid_z_{run_type}.csv'
    rows = []

    if run_type == 'full':
        subs = ["moshiGO_201", "moshiGO_202", "moshiGO_203", "moshiGO_208", "moshiGO_211", "moshiGO_212", "moshiGO_213", "moshiGO_220", "moshiGO_221", "moshiGO_222", "moshiGO_223", "moshiGO_224", "moshiGO_226", "moshiGO_228", "moshiGO_229", "moshiGO_230", "moshiGO_231", "moshiGO_232", "moshiGO_235", "moshiGO_238", "moshiGO_239", "moshiGO_240", "moshiGO_241", "moshiGO_243", "moshiGO_246", "moshiGO_247", "moshiGO_248", "moshiGO_249", "moshiGO_250", "moshiGO_251", "moshiGO_252", "moshiGO_253", "moshiGO_255", "moshiGO_258", "moshiGO_259", "moshiGO_260", "moshiGO_261", "moshiGO_262", "moshiGO_266", "moshiGO_268", "moshiGO_270", "moshiGO_271", "moshiGO_273", "moshiGO_277", "moshiGO_278", "moshiGO_279", "moshiGO_280", "moshiGO_281", "moshiGO_282", "moshiGO_284", "moshiGO_285", "moshiGO_289", "moshiGO_291", "moshiGO_292", "moshiGO_293", "moshiGO_294", "moshiGO_297", "moshiGO_298", "moshiGO_302", "moshiGO_304", "moshiGO_305", "moshiGO_306", "moshiGO_308", "moshiGO_310", "moshiGO_312", "moshiGO_313", "moshiGO_314", "moshiGO_315", "moshiGO_316", "moshiGO_320", "moshiGO_321", "moshiGO_322", "moshiGO_323", "moshiGO_324", "moshiGO_327", "moshiGO_329", "moshiGO_331", "moshiGO_333", "moshiGO_334", "moshiGO_336", "moshiGO_339", "moshiGO_341", "moshiGO_343", "moshiGO_345", "moshiGO_350", "moshiGO_351"]
    elif run_type == 'late':
        subs = ["moshiGO_222", "moshiGO_211", "moshiGO_351", "moshiGO_298", "moshiGO_226", "moshiGO_323", "moshiGO_341", "moshiGO_229", "moshiGO_279", "moshiGO_282", "moshiGO_350", "moshiGO_212", "moshiGO_240", "moshiGO_262", "moshiGO_297", "moshiGO_280", "moshiGO_329", "moshiGO_253", "moshiGO_268", "moshiGO_221", "moshiGO_343", "moshiGO_273", "moshiGO_324", "moshiGO_239", "moshiGO_247", "moshiGO_220", "moshiGO_243", "moshiGO_281", "moshiGO_251", "moshiGO_322", "moshiGO_327", "moshiGO_314", "moshiGO_336", "moshiGO_250", "moshiGO_310", "moshiGO_308", "moshiGO_331", "moshiGO_339", "moshiGO_320", "moshiGO_246", "moshiGO_208", "moshiGO_249", "moshiGO_313", "moshiGO_315", "moshiGO_333", "moshiGO_201", "moshiGO_266", "moshiGO_238", "moshiGO_258", "moshiGO_231", "moshiGO_304", "moshiGO_259", "moshiGO_261", "moshiGO_284", "moshiGO_305", "moshiGO_312", "moshiGO_224", "moshiGO_291", "moshiGO_223", "moshiGO_235", "moshiGO_202", "moshiGO_306", "moshiGO_293", "moshiGO_260", "moshiGO_292", "moshiGO_203", "moshiGO_271", "moshiGO_252", "moshiGO_270", "moshiGO_228", "moshiGO_232", "moshiGO_302"]
    else:
        raise ValueError("run_type must be 'full' or 'late'")

    rois = ['b_erc', 'l_erc', 'r_erc']
    roi_paths = {roi: f'{expdir}/mni/mni_masks/{roi}.nii.gz' for roi in rois}

    z_base = f'{expdir}/mni/late' if run_type == 'late' else f'{expdir}/mni'

    for sub in subs:
        zmap_path = os.path.join(z_base, f"smoothed_{sub}.nii.gz")
        zdata = nib.load(zmap_path).get_fdata()

        row = {'subject': sub}

        for roi_name, roi_path in roi_paths.items():
            roi_data = nib.load(roi_path).get_fdata()
            roi_mask = roi_data > 0
            roi_zvals = zdata[roi_mask]
            row[roi_name] = np.mean(roi_zvals)

        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv(csv_path, index=False)

if __name__ == "__main__":
    # Default to 'full' if no argument is passed
    run_type = sys.argv[1] if len(sys.argv) > 1 else 'full'
    extract_mean_roi_zvals(run_type)