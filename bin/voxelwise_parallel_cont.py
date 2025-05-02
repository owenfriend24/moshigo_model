import pandas as pd
import numpy as np
import nibabel as nib
from nilearn.masking import apply_mask, unmask
import statsmodels.formula.api as smf
import warnings
import time
from joblib import Parallel, delayed
import argparse
from statsmodels.tools.sm_exceptions import ConvergenceWarning

# Suppress annoying warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=ConvergenceWarning)

# Parse chunk ID
parser = argparse.ArgumentParser()
parser.add_argument("--chunk", type=int, default=0, help="Chunk ID (0, 1, 2, 3)")
args = parser.parse_args()
chunk_id = args.chunk

# Load metadata
df = pd.read_csv("/home1/09123/ofriend/analysis/moshigo_model/pca_sl_meta.csv")

# Set '6-9yo' as reference level for age_group
df['age_group'] = pd.Categorical(
    df['age_group'],
    categories=['6-9yo', '10-12yo', 'Adults'],
    ordered=True
)
df['run'] = pd.to_numeric(df['run'])

# Load brain mask
mask_img = nib.load('/scratch/09123/ofriend/moshi/pca_sl/results/group_50_mask.nii.gz')
mask = mask_img.get_fdata() != 0
mask_img = nib.Nifti1Image(mask.astype(np.uint8), affine=mask_img.affine)

# Extract voxelwise data
voxel_data = []
for _, row in df.iterrows():
    img = nib.load(row['path'])
    data = apply_mask(img, mask_img)
    voxel_data.append(data)

voxel_array = np.array(voxel_data)  # shape: (n_obs, n_voxels)

# Split voxels into chunks
n_voxels = voxel_array.shape[1]
n_chunks = 4
chunk_size = n_voxels // n_chunks

start_idx = chunk_id * chunk_size
end_idx = (chunk_id + 1) * chunk_size if chunk_id < n_chunks - 1 else n_voxels

print(f"Running chunk {chunk_id}: voxels {start_idx} to {end_idx} out of {n_voxels}")

voxel_subset = voxel_array[:, start_idx:end_idx]

all_terms = {
    "10-12yo_main": "C(age_group)[T.10-12yo]",
    "Adults_main": "C(age_group)[T.Adults]",
    "run_slope": "run",
    "10-12yo_by_run": "C(age_group)[T.10-12yo]:run",
    "Adults_by_run": "C(age_group)[T.Adults]:run"
}


# Progress tracking setup
progress_counter = [0]
start_time = time.time()

# Define a function to fit one voxel
def fit_voxel(v):
    df_model = df.copy()
    df_model['var_expl'] = voxel_subset[:, v]
    try:
        model = smf.mixedlm("var_expl ~ C(age_group) * run", df_model, groups=df_model["subject"])
        fit = model.fit(reml=False)
        pvals = fit.pvalues
        result = {key: 1 - pvals.get(term, np.nan) for key, term in all_terms.items()}
    except:
        result = {key: np.nan for key in all_terms}

    return result

# Run in parallel
n_jobs = 12
results = Parallel(n_jobs=n_jobs, verbose=10)(
    delayed(fit_voxel)(v) for v in range(voxel_subset.shape[1])
)

# Reformat results
results_dict = {key: [] for key in all_terms}
for res in results:
    for key in res:
        results_dict[key].append(res[key])

# Save (1 - p) maps
output_dir = "/scratch/09123/ofriend/moshi/pca_sl/results/"

for key, inv_p_vals in results_dict.items():
    np.save(f"{output_dir}/group_{key}_chunk{chunk_id}_1minuspmap.npy", np.array(inv_p_vals, dtype=np.float32))


terms = ["10-12yo_main", "Adults_main", "run_slope", "10-12yo_by_run", "Adults_by_run"]

for term in terms:
    chunks = []
    for chunk_id in range(4):
        chunk = np.load(f"{output_dir}/group_{term}_chunk{chunk_id}_1minuspmap.npy")
        chunks.append(chunk)
    full_data = np.concatenate(chunks)
    final_img = unmask(full_data, mask_img)
    final_img.to_filename(f"{output_dir}/group_{term}_1minuspmap_FULL.nii.gz")
# for key, inv_p_vals in results_dict.items():
#     img = unmask(np.array(inv_p_vals, dtype=np.float32), mask_img)
#     img.to_filename(f"{output_dir}/group_{key}_chunk{chunk_id}_1minuspmap.nii.gz")
