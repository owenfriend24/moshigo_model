
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
from scipy.spatial import procrustes
from itertools import combinations
from collections import defaultdict
import matplotlib.pyplot as plt


# --- USER INPUTS ---
expdir = '/corral-repl/utexas/prestonlab/moshiGO1'
meta_csv = '/home1/09123/ofriend/analysis/moshigo_model/pca_sl_meta_6run.csv'


for cluster_name in ['masked_hip', 'unmasked_hip', 'ifg']:
    output_fig = f'/home1/09123/ofriend/analysis/moshigo_model/pca_trajectories_by_agegroup_{cluster_name}.png'
    saved_df_path = f'/home1/09123/ofriend/analysis/moshigo_model/pca_trajectories_latents_{cluster_name}.csv'
    # Check if the dataframe already exists
    if os.path.exists(saved_df_path):
        print("Loading existing latent trajectory dataframe...")
        traj_df = pd.read_csv(saved_df_path)
    else:
        print("Extracting neural data and computing latent trajectories...")

        # Load metadata
        meta_df = pd.read_csv(meta_csv)
        meta_df = meta_df.drop_duplicates(subset='subject')
        trajectories = []

        for idx, row in meta_df.iterrows():
            sub = row['subject']
            age = row['age_group']

            cluster_path = f'/scratch/09123/ofriend/moshi/pca_sl/results/moshiGO_{sub}/moshiGO_{sub}_run-1_MASK_cluster-{cluster_name}.nii.gz'
            if not os.path.exists(cluster_path):
                continue

            cluster_mask = nib.load(cluster_path)
            cluster_mask_data = cluster_mask.get_fdata() > 0
            mask_img = nib.Nifti1Image(cluster_mask_data.astype(np.uint8), affine=cluster_mask.affine)

            for item in [1, 2, 3, 4]:
                for run in [1, 2, 3, 4, 5, 6]:
                    func_path = f'{expdir}/moshiGO_{sub}/RSAmodel/betaseries/moshiGO_{run}_all.nii.gz'
                    if not os.path.exists(func_path):
                        continue

                    img = nib.load(func_path)
                    data = apply_mask(img, mask_img)  # shape: (4 items, voxels)
                    if data.shape[0] != 4:
                        continue

                    pca = PCA(n_components=3)
                    pcs = pca.fit_transform(data)
                    pc1, pc2, pc3 = pcs[item - 1]  # Get this specific item's projection

                    trajectories.append({
                        'Subject': sub,
                        'AgeGroup': age,
                        'Run': run,
                        'Item': item,
                        'PC1': pc1,
                        'PC2': pc2,
                        'PC3': pc3
                    })

        # Save all trajectories
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
    markers = ['o', 's', 'D', '^', 'v', 'P']  # run 1, 2, 3

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





    # === PLOT: Run 6 Only (Item Endpoints) ===
    run6_df = avg_df[avg_df['Run'] == 6].copy()

    fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharex=True, sharey=True)
    markers = ['o', 's', 'D', '^', 'v', 'P']  # update if needed
    age_groups = ['6-9yo', '10-12yo', 'Adults']
    palette = sns.color_palette("tab10", n_colors=4)

    for ax, age_group in zip(axes, age_groups):
        sub_df = run6_df[run6_df['AgeGroup'] == age_group]
        for item in [1, 2, 3, 4]:
            point = sub_df[sub_df['Item'] == item]
            if not point.empty:
                ax.scatter(point['PC1'], point['PC2'],
                           color=palette[item - 1],
                           marker=markers[5],  # marker for Run 6
                           s=100,
                           label=f'Item {item}')
        ax.set_title(f"Run 6 - Age Group: {age_group}")
        ax.set_xlabel("PC1")
        ax.set_ylabel("PC2")

    handles = [Line2D([0], [0], marker=markers[5], color='w',
                      label=f'Item {i+1}', markerfacecolor=palette[i], markersize=10)
               for i in range(4)]
    fig.legend(handles, [f'Item {i+1}' for i in range(4)],
               loc='center right', title='Item', fontsize=10)
    fig.subplots_adjust(right=0.85)

    plt.suptitle("Smoothed PCA Positions (Run 6 Only)", fontsize=16)
    plt.tight_layout(rect=[0, 0, 0.85, 0.95])
    plt.savefig(f'/home1/09123/ofriend/analysis/moshigo_model/pca_run6_points_by_agegroup_{cluster_name}.png')
    plt.show()


