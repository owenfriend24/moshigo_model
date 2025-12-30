
import numpy as np
import pandas as pd
import nibabel as nib
import os
from nilearn.masking import apply_mask
from sklearn.decomposition import PCA


expdir = '/corral-repl/utexas/prestonlab/moshiGO1'
meta_csv = '/home1/09123/ofriend/analysis/moshigo_model/pca_sl_meta_6run.csv'


for cluster_name in ['hip_cluster_acc_masked']:
    saved_df_path = f'/home1/09123/ofriend/analysis/moshigo_model/pca_trajectories_latents_{cluster_name}.csv'

    if os.path.exists(saved_df_path):
        print("Loading existing dataframe...")
        traj_df = pd.read_csv(saved_df_path)
    else:
        print("Extracting neural data and computing neural space embeddings...")

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
                    pc1, pc2, pc3 = pcs[item - 1]  # get this specific item's projection

                    trajectories.append({
                        'Subject': sub,
                        'AgeGroup': age,
                        'Run': run,
                        'Item': item,
                        'PC1': pc1,
                        'PC2': pc2,
                        'PC3': pc3
                    })

        # save all trajectories
        traj_df = pd.DataFrame(trajectories)
        traj_df.to_csv(saved_df_path, index=False)
        print(f"Saved latent trajectory dataframe to: {saved_df_path}")

