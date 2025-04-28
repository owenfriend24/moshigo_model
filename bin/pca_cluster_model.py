import nibabel as nib
import numpy as np
import statsmodels.formula.api as smf
import pandas as pd


ref = pd.read_csv("/home1/09123/ofriend/analysis/moshigo_model/pca_sl_meta.csv")

df = ref.copy()
subject_maps = df['path'] # PCA variance maps

cluster_dir='/scratch/09123/ofriend/moshi/pca_sl/results/cluster_masks'
cluster_1 = nib.load(f"{cluster_dir}/cluster_hip.nii.gz").get_fdata().astype(bool)
cluster_2 = nib.load(f"{cluster_dir}/cluster_l_ifg.nii.gz").get_fdata().astype(bool)
cluster_3 = nib.load(f"{cluster_dir}/cluster_r_ifg.nii.gz").get_fdata().astype(bool)
cluster_4 = nib.load(f"{cluster_dir}/cluster_lpfc.nii.gz").get_fdata().astype(bool)
cluster_5 = nib.load(f"{cluster_dir}/cluster_postcentral.nii.gz").get_fdata().astype(bool)

cluster_index = 1
for cluster_mask in [cluster_1, cluster_2, cluster_3, cluster_4, cluster_5]:
    means = []
    for i, path in enumerate(subject_maps):
        img = nib.load(path).get_fdata()
        mean_val = np.mean(img[cluster_mask])
        means.append(mean_val)

    df[f'cluster_{cluster_index}_mean'] = means

    model = smf.mixedlm(f"cluster_{cluster_index}_mean ~ C(age_group) * C(run)", df, groups=df["subject"])
    result = model.fit()
    print(f'RAN MODEL FOR VARIANCE EXPLAINED BY PC1 AND PC2 IN CLUSTER {cluster_index}:')
    print()
    print(result.summary())
    print()
    cluster_index +=1
df.to_csv("/home1/09123/ofriend/analysis/moshigo_model/pca_cluster_model_results.csv")
