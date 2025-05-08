import numpy as np
import pandas as pd
import nibabel as nib
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
import os
from nilearn.masking import apply_mask

for cluster_name in ['masked_hip']:

    expdir = '/corral-repl/utexas/prestonlab/moshiGO1'
    subject_metadata_csv = '/home1/09123/ofriend/analysis/moshigo_model/pca_sl_meta_6run_acc.csv'
    output_plot = f'/home1/09123/ofriend/analysis/moshigo_model/test_pca_plot_{cluster_name}.png'
    output_plot_avg = f'/home1/09123/ofriend/analysis/moshigo_model/test_pca_plot_average_{cluster_name}.png'

    meta_df = pd.read_csv(subject_metadata_csv)
    all_rows = []

    for idx, row in meta_df.iterrows():
        subject_id = row['subject']
        age_group = row['age_group']

        cluster_mask_path =  f'/scratch/09123/ofriend/moshi/pca_sl/results/moshiGO_{subject_id}/moshiGO_{subject_id}_run-1_MASK_cluster-{cluster_name}.nii.gz'

        cluster_img = nib.load(cluster_mask_path)
        cluster_mask_data = cluster_img.get_fdata() > 0
        mask_img = nib.Nifti1Image(cluster_mask_data.astype(np.uint8), affine=cluster_img.affine)

        for run in [1, 2, 3, 4, 5, 6]:
            betaseries_path = f'{expdir}/moshiGO_{subject_id}/RSAmodel/betaseries/moshiGO_{run}_all.nii.gz'
            if not os.path.exists(betaseries_path):
                print(f"Missing: {betaseries_path}")
                continue

            img = nib.load(betaseries_path)
            masked_data = apply_mask(img, mask_img)

            if masked_data.shape[0] != 4:
                print(f"Unexpected shape for {subject_id} run {run}: {masked_data.shape}")
                continue

            pca = PCA(n_components=2)
            pcs = pca.fit_transform(masked_data)

            for item_idx in range(4):
                all_rows.append({
                    'AgeGroup': age_group,
                    'Run': run,
                    'Item': item_idx + 1,
                    'PC1': pcs[item_idx, 0],
                    'PC2': pcs[item_idx, 1]
                })

    plot_df = pd.DataFrame(all_rows)
    avg_df = plot_df.groupby(['AgeGroup', 'Run', 'Item']).mean().reset_index()

    # === Plot by Age Group ===
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
    plt.close()

    # === Grand Average Across Age Groups ===
    grand_avg_df = plot_df.groupby(['Run', 'Item']).mean().reset_index()

    plt.figure(figsize=(6, 6))
    sns.scatterplot(
        data=grand_avg_df,
        x="PC1", y="PC2",
        hue="Item",
        style="Run",
        s=100
    )
    plt.title("PCA Space: Item Representations by Run (Averaged Across All Groups)")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.legend(title="Item / Run")
    plt.tight_layout()
    plt.savefig(output_plot_avg)
    plt.show()
