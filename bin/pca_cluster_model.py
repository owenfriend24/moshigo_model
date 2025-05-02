#!/usr/bin/env python

import nibabel as nib
import numpy as np
import statsmodels.formula.api as smf
import pandas as pd
import subprocess


ref = pd.read_csv("/home1/09123/ofriend/analysis/moshigo_model/pca_sl_meta_6run.csv")

df = ref.copy()
subject_maps = df['func_path'] # PCA variance maps

cluster_dir='/scratch/09123/ofriend/moshi/pca_sl/results'
cluster_1_path = f"{cluster_dir}/hip_7_mask.nii.gz"
# cluster_1 = nib.load(cluster_1_path).get_fdata().astype(bool)

cluster_2_path = f"{cluster_dir}/hip_13_mask.nii.gz"
# cluster_2 = nib.load(cluster_1_path).get_fdata().astype(bool)

cluster_3_path = f"{cluster_dir}/hip_5_mask.nii.gz"
# cluster_3 = nib.load(cluster_1_path).get_fdata().astype(bool)


# cluster_2 = nib.load(f"{cluster_dir}/cluster_l_ifg.nii.gz").get_fdata().astype(bool)
# cluster_3 = nib.load(f"{cluster_dir}/cluster_r_ifg.nii.gz").get_fdata().astype(bool)
# cluster_4 = nib.load(f"{cluster_dir}/cluster_lpfc.nii.gz").get_fdata().astype(bool)
# cluster_5 = nib.load(f"{cluster_dir}/cluster_postcentral.nii.gz").get_fdata().astype(bool)

cluster_index = 1
for cluster_path in [cluster_1_path, cluster_2_path, cluster_3_path]: #, cluster_2, cluster_3, cluster_4, cluster_5]:
    means = []
    for i, path in enumerate(subject_maps):
        sub = df.loc[i, 'subject']
        run = df.loc[i, 'run']

        #back project the cluster mask into functional space for each subject
        warp_path = f'/corral-repl/utexas/prestonlab/moshiGO1/moshiGO_{sub}/anatomy/antsreg/transforms/brain2MNI_1mm_InverseWarp.nii.gz'
        affine_path = f'/corral-repl/utexas/prestonlab/moshiGO1/moshiGO_{sub}/anatomy/antsreg/transforms/brain2MNI_1mm_Affine.txt'
        # affine followed by ,1 for inverse
        out_path = f"{cluster_dir}/moshiGO_{sub}/moshiGO_{sub}_run-{run}_MASK_cluster-{cluster_index}.nii.gz"

        cmd = [
            'antsApplyTransforms', '-d', '3',
            '-i', cluster_path,
            '-o', out_path,
            '-r', path,
            '-n', 'NearestNeighbor',
            '-t', f'[{affine_path},1]',
            '-t', warp_path
        ]
        subprocess.run(cmd, check = True)

        # now load the functional image and mask
        img = nib.load(path).get_fdata()
        mask = nib.load(out_path).get_fdata().astype(bool)

        # mask the data and exclude voxels without observations
        masked_vals = img[mask]
        masked_vals = masked_vals[masked_vals > 0]
        mean_val = np.nanmean(masked_vals)
        means.append(mean_val)
    print("transformed clusters")
    df[f'cluster_{cluster_index}_mean'] = means
    print("running model ...")
    model = smf.mixedlm(f"cluster_{cluster_index}_mean ~ C(age_group) * run", df, groups=df["subject"])
    result = model.fit()
    print(f'RAN MODEL FOR VARIANCE EXPLAINED BY PC1 AND PC2 IN CLUSTER {cluster_index}:')
    print()
    print(result.summary())
    print()
    cluster_index +=1
df.to_csv(f"/home1/09123/ofriend/analysis/moshigo_model/pca_cluster_hip_{cluster_index}_model_results.csv")
