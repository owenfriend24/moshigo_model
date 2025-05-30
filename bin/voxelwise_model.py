import pandas as pd
import numpy as np
import nibabel as nib
from nilearn.masking import apply_mask, unmask
import statsmodels.formula.api as smf
import warnings
from statsmodels.tools.sm_exceptions import ConvergenceWarning
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=ConvergenceWarning)
# Load metadata
df = pd.read_csv("/home1/09123/ofriend/analysis/moshigo_model/pca_sl_meta.csv")

# Set '6-9yo' as reference level for age_group
df['age_group'] = pd.Categorical(
    df['age_group'],
    categories=['6-9yo', '10-12yo', 'Adults'],
    ordered=True
)

# Load brain mask
mask_img = nib.load('/home1/09123/ofriend/analysis/moshigo_model/mni_gm_mask.nii.gz')
mask = mask_img.get_fdata() != 0
mask_img = nib.Nifti1Image(mask.astype(np.uint8), affine=mask_img.affine)

# Extract voxelwise data
voxel_data = []
for _, row in df.iterrows():
    img = nib.load(row['path'])
    data = apply_mask(img, mask_img)
    voxel_data.append(data)

voxel_array = np.array(voxel_data)  # shape: (n_obs, n_voxels)

# Define interaction and main effect terms to extract
interaction_terms = {
    "10-12yo:run2": "C(age_group)[T.10-12yo]:C(run)[T.2]",
    "10-12yo:run3": "C(age_group)[T.10-12yo]:C(run)[T.3]",
    "Adults:run2": "C(age_group)[T.Adults]:C(run)[T.2]",
    "Adults:run3": "C(age_group)[T.Adults]:C(run)[T.3]",
}

main_effects = {
    "10-12yo_main": "C(age_group)[T.10-12yo]",
    "Adults_main": "C(age_group)[T.Adults]",
    "run2_main": "C(run)[T.2]",
    "run3_main": "C(run)[T.3]",
}

# Combine all terms
all_terms = {**interaction_terms, **main_effects}
results_dict = {key: [] for key in all_terms}

# Fit LME model per voxel
df_model = df.copy()
for v in range(voxel_array.shape[1]):
    df_model['var_expl'] = voxel_array[:, v]
    try:
        model = smf.mixedlm("var_expl ~ C(age_group) * C(run)", df_model, groups=df_model["subject"])
        fit = model.fit(reml=False)
        pvals = fit.pvalues
        for key, term in all_terms.items():
            pval = pvals.get(term, np.nan)
            results_dict[key].append(1 - pval if not np.isnan(pval) else np.nan)
    except:
        for key in results_dict:
            results_dict[key].append(np.nan)

# Save (1 - p) maps
for key, inv_p_vals in results_dict.items():
    img = unmask(np.array(inv_p_vals, dtype=np.float32), mask_img)
    img.to_filename(f"/scratch/09123/ofriend/moshi/pca_sl/results/group_{key}_1minuspmap.nii.gz")