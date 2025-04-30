import numpy as np
import pandas as pd
import nibabel as nib
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
import os
from nilearn.masking import apply_mask

# Set your paths
expdir = '/corral-repl/utexas/prestonlab/moshiGO1'
cluster_mask_path = f'/scratch/09123/ofriend/moshi/pca_sl/results/ifg_mask.nii.gz'
subject_metadata_csv = '/home1/09123/ofriend/analysis/moshigo_model/pca_sl_meta.csv'
output_plot = "/path/to/save_pca_plot.png"

# Load cluster mask
cluster_img = nib.load(cluster_mask_path)
cluster_mask_data = cluster_img.get_fdata() > 0
mask_img = nib.Nifti1Image(cluster_mask_data.astype(np.uint8), affine=cluster_img.affine)

# Load subject metadata
meta_df = pd.read_csv(subject_metadata_csv)

# Initialize list to collect data
all_rows = []

# Loop over subjects
for idx, row in meta_df.iterrows():
    subject_id = row['subject']
    age_group = row['age_group']

    for run in [1, 2, 3]:
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
                'Subject': subject_id,
                'AgeGroup': age_group,
                'Run': run,
                'Item': item_idx + 1,
                'PC1': pcs[item_idx, 0],
                'PC2': pcs[item_idx, 1]
            })

# Build full DataFrame
plot_df = pd.DataFrame(all_rows)

# Plot
plt.figure(figsize=(10, 8))
sns.scatterplot(
    data=plot_df,
    x='PC1', y='PC2',
    hue='AgeGroup',
    style='Run',
    s=100
)
plt.title("PCA Space: Four Items by Age Group and Run")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(output_plot)
plt.show()
