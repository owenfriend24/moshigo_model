import numpy as np
import pandas as pd
import nibabel as nib
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
import os
from nilearn.masking import apply_mask

cluster_name = 'cluster-1'

expdir = '/corral-repl/utexas/prestonlab/moshiGO1'
subject_metadata_csv = '/home1/09123/ofriend/analysis/moshigo_model/pca_sl_meta_6run.csv'
output_plot = '/home1/09123/ofriend/analysis/moshigo_model/test_pca_plot.png'

# Load subject metadata
meta_df = pd.read_csv(subject_metadata_csv)

# Initialize list to collect data
all_rows = []

# Loop over subjects
for idx, row in meta_df.iterrows():
    subject_id = row['subject']
    age_group = row['age_group']

    # assumes you've already back-projected clusters into subject space
    cluster_mask_path =  f'/scratch/09123/ofriend/moshi/pca_sl/results/moshiGO_{subject_id}/moshiGO_{subject_id}_run-1_MASK_{cluster_name}.nii.gz'
    cluster_img = nib.load(cluster_mask_path)
    cluster_mask_data = cluster_img.get_fdata() > 0
    mask_img = nib.Nifti1Image(cluster_mask_data.astype(np.uint8), affine=cluster_img.affine)

    for run in [1, 2, 3, 4, 5, 6]:
        # Build the betaseries filepath
        betaseries_path = f'{expdir}/moshiGO_{subject_id}/RSAmodel/betaseries/moshiGO_{run}_all.nii.gz'

        if not os.path.exists(betaseries_path):
            print(f"Missing: {betaseries_path}")
            continue

        # Load betaseries
        img = nib.load(betaseries_path)
        img_data = img.get_fdata()  # Expect shape (x, y, z, 4)

        # Apply cluster mask
        masked_data = apply_mask(img, mask_img)  # Shape: (n_samples=4, n_voxels)

        if masked_data.shape[0] != 4:
            print(f"Unexpected shape for {subject_id} run {run}: {masked_data.shape}")
            continue

        # Perform PCA across items
        pca = PCA(n_components=2)
        pcs = pca.fit_transform(masked_data)  # shape (4 items, 2 PCs)

        # Store results
        for item_idx in range(4):
            all_rows.append({
                'AgeGroup': age_group,
                'Run': run,
                'Item': item_idx + 1,
                'PC1': pcs[item_idx, 0],
                'PC2': pcs[item_idx, 1]
            })

# Build full DataFrame
plot_df = pd.DataFrame(all_rows)

# Average across subjects
avg_df = plot_df.groupby(['AgeGroup', 'Run', 'Item']).mean().reset_index()

g = sns.relplot(
    data=avg_df,
    x="PC1", y="PC2",
    col="AgeGroup",
    hue="Item",
    style="Run",
    kind="scatter",
    height=5, aspect=1,
    s=100
)

g.set_titles(col_template="Age Group: {col_name}")
g.fig.subplots_adjust(top=0.85)
g.fig.suptitle("PCA Space: Item Representations by Run (Averaged by Age Group)")
g.savefig(output_plot)
plt.show()
