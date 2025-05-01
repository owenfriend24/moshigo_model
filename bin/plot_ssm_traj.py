
import numpy as np
import pandas as pd
import nibabel as nib
import os
from nilearn.masking import apply_mask
from sklearn.decomposition import PCA
from pykalman import KalmanFilter
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D


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


# Set up plot
sns.set(style="white", context="talk")
fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharex=True, sharey=True)
age_groups = ['6-9yo', '10-12yo', 'Adults']
palette = sns.color_palette("tab10", n_colors=4)
markers = ['o', 's', 'D']  # run 1, 2, 3

for ax, age_group in zip(axes, age_groups):
    sub_df = avg_df[avg_df['AgeGroup'] == age_group]
    for item in [1, 2, 3, 4]:
        segment = sub_df[sub_df['Item'] == item].sort_values('Run')
        if not segment.empty:
            # Plot line connecting the 3 runs for this item
            ax.plot(segment['PC1'], segment['PC2'],
                    color=palette[item - 1],
                    linestyle='-', linewidth=2, alpha=0.9)

            # Plot individual run points with different shapes
            for _, row in segment.iterrows():
                ax.plot(row['PC1'], row['PC2'],
                        marker=markers[row['Run'] - 1],
                        color=palette[item - 1],
                        markersize=8,
                        linestyle='None')

    ax.set_title(f"Age Group: {age_group}")
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")

# Create custom legends
item_legend = [Line2D([0], [0], color=palette[i], lw=3, label=f'Item {i+1}') for i in range(4)]
run_legend = [Line2D([0], [0], color='gray', marker=markers[i], linestyle='None', markersize=8, label=f'Run {i+1}') for i in range(3)]

fig.legend(item_legend + run_legend,
           [leg.get_label() for leg in item_legend + run_legend],
           loc='center right', title='Item / Run', fontsize=10)
fig.subplots_adjust(right=0.85)

plt.suptitle("Average Smoothed PCA Trajectories by Age Group\n(Colors = Items, Shapes = Runs)", fontsize=16)
plt.tight_layout(rect=[0, 0, 0.85, 0.95])
plt.savefig(output_fig)
plt.show()





# === PLOT: Run 3 Only (Item Endpoints) ===
run3_df = avg_df[avg_df['Run'] == 3].copy()

fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharex=True, sharey=True)

for ax, age_group in zip(axes, age_groups):
    sub_df = run3_df[run3_df['AgeGroup'] == age_group]
    for item in [1, 2, 3, 4]:
        point = sub_df[sub_df['Item'] == item]
        if not point.empty:
            ax.scatter(point['PC1'], point['PC2'],
                       color=palette[item - 1],
                       marker=markers[2],  # Run 3 marker: 'D'
                       s=100,
                       label=f'Item {item}')
    ax.set_title(f"Run 3 - Age Group: {age_group}")
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")

# Clean up legend
handles = [Line2D([0], [0], marker='D', color='w',
                  label=f'Item {i+1}', markerfacecolor=palette[i], markersize=10)
           for i in range(4)]
fig.legend(handles, [f'Item {i+1}' for i in range(4)],
           loc='center right', title='Item', fontsize=10)
fig.subplots_adjust(right=0.85)

plt.suptitle("Smoothed PCA Positions (Run 3 Only)", fontsize=16)
plt.tight_layout(rect=[0, 0, 0.85, 0.95])
plt.savefig('/home1/09123/ofriend/analysis/moshigo_model/pca_run3_points_by_agegroup.png')
plt.show()


from scipy.spatial import procrustes
from itertools import combinations
from collections import defaultdict

# Group trajectories by subject
grouped = traj_df.groupby(['Subject', 'AgeGroup'])

# Collect subject trajectories
trajectories_by_group = defaultdict(list)

for (sub, age), group in grouped:
    subj_traj = group.sort_values('Timepoint')[['PC1', 'PC2']].values
    if subj_traj.shape == (12, 2):  # ensure full length
        trajectories_by_group[age].append(subj_traj)

# Measure average Procrustes distance within each age group
from scipy.spatial.distance import euclidean

group_scores = {}
for age, traj_list in trajectories_by_group.items():
    dists = []
    for a, b in combinations(traj_list, 2):
        _, _, disparity = procrustes(a, b)
        dists.append(disparity)
    group_scores[age] = np.mean(dists) if dists else np.nan

# Print scores (lower = more coherent)
print("\nAverage within-group trajectory distances (Procrustes):")
for age, score in group_scores.items():
    print(f"{age}: {score:.4f}")