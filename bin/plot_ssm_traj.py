
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

        cluster_path = f'/scratch/09123/ofriend/moshi/pca_sl/results/moshiGO_{sub}/moshiGO_{sub}_run-1_MASK_cluster-1.nii.gz'
        if not os.path.exists(cluster_path):
            continue

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
            data = apply_mask(img, mask_img)
            if data.shape[0] != 4:
                continue

            pca = PCA(n_components=2)
            pcs = pca.fit_transform(data)
            all_items.append(pcs)
            run_labels.extend([run] * 4)
            item_labels.extend([1, 2, 3, 4])

        if len(all_items) != 3:
            continue

        seq = np.concatenate(all_items, axis=0)

        kf = KalmanFilter(transition_matrices=np.eye(2),
                          observation_matrices=np.eye(2),
                          initial_state_mean=seq[0],
                          n_dim_obs=2, n_dim_state=2)
        smoothed_state_means, _ = kf.smooth(seq)

        for i in range(len(smoothed_state_means)):
            trajectories.append({
                'Subject': sub,
                'AgeGroup': age,
                'Timepoint': i + 1,
                'Run': run_labels[i],
                'Item': item_labels[i],
                'PC1': smoothed_state_means[i, 0],
                'PC2': smoothed_state_means[i, 1]
            })

    traj_df = pd.DataFrame(trajectories)
    traj_df.to_csv(saved_df_path, index=False)
    print(f"Saved latent trajectory dataframe to: {saved_df_path}")

# Average across subjects within age group, run, and item
avg_df = traj_df.groupby(['AgeGroup', 'Run', 'Item']).mean(numeric_only=True).reset_index()

# Create a unique label for legend clarity
avg_df['Label'] = avg_df['Item'].astype(str) + '_item_run' + avg_df['Run'].astype(str)

# Plot
sns.set(style="white", context="talk")
fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharex=True, sharey=True)
age_groups = ['6-9yo', '10-12yo', 'Adults']
palette = sns.color_palette("tab10", n_colors=4)
markers = ['o', 's', 'D']

for ax, age_group in zip(axes, age_groups):
    sub_df = avg_df[avg_df['AgeGroup'] == age_group]
    for item in [1, 2, 3, 4]:
        for run in [1, 2, 3]:
            segment = sub_df[(sub_df['Item'] == item) & (sub_df['Run'] == run)]
            if not segment.empty:
                ax.plot(segment['PC1'], segment['PC2'], label=f'Item {item}, Run {run}',
                        color=palette[item - 1], marker=markers[run - 1], linestyle='-', markersize=6)
    ax.set_title(f"Age Group: {age_group}")
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")

# Global legend
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='center right', title='Item & Run', fontsize=9)
fig.subplots_adjust(right=0.85)

plt.suptitle("Mean Kalman-smoothed PCA Trajectories by Age Group (Color=Item, Marker=Run)", fontsize=16)
plt.tight_layout(rect=[0, 0, 0.85, 0.95])
plt.savefig(output_fig)
plt.show()
