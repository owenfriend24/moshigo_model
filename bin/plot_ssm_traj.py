import numpy as np
import pandas as pd
import nibabel as nib
import os
from nilearn.masking import apply_mask
from sklearn.decomposition import PCA
from ssm import HMM
import matplotlib.pyplot as plt
import seaborn as sns

# --- USER INPUTS ---
expdir = '/corral-repl/utexas/prestonlab/moshiGO1'
meta_csv = '/home1/09123/ofriend/analysis/moshigo_model/pca_sl_meta.csv'
output_fig = '/home1/09123/ofriend/analysis/moshigo_model/pca_trajectories_by_agegroup.png'
saved_df_path = '/home1/09123/ofriend/analysis/moshigo_model/pca_trajectories_latents.csv'

# Check if the dataframe already exists
if os.path.exists(saved_df_path):
    print("Loading existing latent trajectory dataframe...")
    traj_df = pd.read_csv(saved_df_path)
else:
    print("Extracting neural data and computing latent trajectories...")

    # Load metadata and mask
    meta_df = pd.read_csv(meta_csv)

    # Collect latent trajectories
    trajectories = []

    for idx, row in meta_df.iterrows():
        sub = row['subject']
        age = row['age_group']

        # assumes cluster masks already created for now
        cluster_path = f'/scratch/09123/ofriend/moshi/pca_sl/results/moshiGO_{sub}/moshiGO_{sub}_run-1_MASK_cluster-1.nii.gz'
        cluster_mask = nib.load(cluster_path)
        cluster_mask_data = cluster_mask.get_fdata() > 0
        mask_img = nib.Nifti1Image(cluster_mask_data.astype(np.uint8), affine=cluster_mask.affine)

        all_items = []
        for run in [1, 2, 3]:
            func_path = f'{expdir}/moshiGO_{sub}/RSAmodel/betaseries/moshiGO_{run}_all.nii.gz'
            if not os.path.exists(func_path):
                continue

            img = nib.load(func_path)
            data = apply_mask(img, mask_img)  # shape (4, voxels)
            if data.shape[0] != 4:
                continue

            pca = PCA(n_components=2)
            pcs = pca.fit_transform(data)  # shape (4, 2)
            all_items.append(pcs)

        if len(all_items) != 3:
            continue

        seq = np.concatenate(all_items, axis=0)  # shape (12, 2)

        # Fit simple linear-Gaussian state space model
        model = HMM(K=3, D=2, observations="gaussian")
        model.fit(seq, method="em", num_iters=50, initialize=True)
        z, x = model.sample(len(seq))
        inferred_states = model.most_likely_states(seq)
        smoothed_means = model.observations.mus[inferred_states]  # (T, 2)

        for i, (pc1, pc2) in enumerate(smoothed_means):
            trajectories.append({
                'Subject': sub,
                'AgeGroup': age,
                'Timepoint': i + 1,
                'PC1': pc1,
                'PC2': pc2
            })

    # Convert to DataFrame
    traj_df = pd.DataFrame(trajectories)
    traj_df.to_csv(saved_df_path, index=False)
    print(f"Saved latent trajectory dataframe to: {saved_df_path}")

# Average per group
avg_traj = traj_df.groupby(['AgeGroup', 'Timepoint']).mean().reset_index()

# Plot
plt.figure(figsize=(10, 6))
sns.lineplot(data=avg_traj, x='PC1', y='PC2', hue='AgeGroup', style='AgeGroup', markers=True)
plt.title("Smoothed PCA Trajectories by Age Group")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.savefig(output_fig)
plt.show()