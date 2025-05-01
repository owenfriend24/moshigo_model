
import numpy as np
import pandas as pd
import nibabel as nib
import os
from nilearn.masking import apply_mask
from sklearn.decomposition import PCA
from pykalman import KalmanFilter
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

    # Load metadata
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
        run_labels = []
        item_labels = []

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
            run_labels.extend([run] * 4)
            item_labels.extend([1, 2, 3, 4])

        if len(all_items) != 3:
            continue

        seq = np.concatenate(all_items, axis=0)  # shape (12, 2)

        # Kalman smoothing
        kf = KalmanFilter(transition_matrices=np.eye(2),
                         observation_matrices=np.eye(2),
                         initial_state_mean=seq[0],
                         n_dim_obs=2, n_dim_state=2)

        smoothed_state_means, _ = kf.smooth(seq)

        for i, (pc1, pc2) in enumerate(smoothed_state_means):
            trajectories.append({
                'Subject': sub,
                'AgeGroup': age,
                'Timepoint': i + 1,
                'Run': run_labels[i],
                'Item': item_labels[i],
                'PC1': pc1,
                'PC2': pc2
            })

    # Convert to DataFrame
    traj_df = pd.DataFrame(trajectories)
    traj_df.to_csv(saved_df_path, index=False)
    print(f"Saved latent trajectory dataframe to: {saved_df_path}")

# Average across subjects within age group, timepoint, run, and item
avg_df = traj_df.groupby(['AgeGroup', 'Timepoint', 'Run', 'Item']).mean(numeric_only=True).reset_index()

# Plot with three panels (facets), color by item, shape by run
sns.set(style="white", context="talk")
g = sns.FacetGrid(avg_df, col="AgeGroup", hue="Item", height=5, aspect=1.1)
g.map_dataframe(sns.scatterplot, x="PC1", y="PC2", style="Run", s=100)
g.add_legend()
g.set_titles(col_template="Age Group: {col_name}")
plt.subplots_adjust(top=0.85)
g.fig.suptitle("Mean Kalman-smoothed PCA Trajectories by Age Group, Item, and Run")
plt.savefig(output_fig)
plt.show()