## Compression of spatial information into low-dimensional cognitive maps

* to identify regions which compress spatial information across the task (and which do so differently by age group), we use voxelwise mixed-effects regression (Mack et al., 2020)
* to summarize:
   1) for item-level representations within each subject, we iteratively sweep a searchlight sphere across the brain, perform PCA, and exteract the % of variance explained by the top 2 principal components
   2) after transforming resulting variance maps into template space, we again iteratively sweet across the brain and implement a mixed-effects model with terms for age group, run, their interaction, and overall task performance, along with subject-level random intercept terms. 
   3) from the above comparison, we compute (1-p) maps to identify contiguous clusters in which we find an age group by run interaction
   4) finally, we back-project the corrected cluster from above (in the hippocampal tail) into each subject's native space to extract changes in variance and similarity between items
* this requires several millions of comparisons and must be implemented in parallel in high-performance computing (HPC) environment

---

### 1) generate variance maps via PCA to assess dimensionality reduction (fix phase 1 vs 2)
* here we assess the % of variance explained by the top two principal components (the minimum required to represent Euclidean distances) to identify regions which compress behaviorally-relevant information into cognitive maps
* input data includes four item-specific neural activity patterns per run (betaseries images) estimated with item-specific GLMs (see Mumford et al., 2012)
* we iteratively sweep a searchlight sphere (3-voxel radius) across these images and extract the % of variance captured by top 2 PC's, averaging across items within run, resulting in one variance map per run per subject
* variance maps are then transformed to template space for voxelwise mixed-effects regression
```
pca_sl.py $subject $brain_mask
```
see (link)[]

or use below to perform searchlight and transformation in same step
```
run_sl_transform.sh
```

---

### 2) perform voxelwise mixed-effects regression to identify regions demonstrating age group/run interaction in compression
* in template space, we iteratively sweep a searchlight sphere (3-voxel radius) across a concatenated 4D image with all subjects and fit a mixed-effects model within that sphere
   * variance_explained = age_group*run + task_performance + (1|subject)
* this requires millions of comparisons, so we chunk the brain into fourths which can run in parallel
* output = (1-p) maps for each coefficient in the model
  * since we are searching for regions which show age differences in compression, we are primarily interested in voxels demonstrating significant age-group/run interaction
```
voxelwise_parallel_6run_acc.py
```
see (link)[]
* finally, perform cluster correction identically to other RSA results (see manuscript), refine by taking intersection with anatomical hippocampus, and reverse-normalize cluster into each participant's native space for following analyses

### 3) from the identified compression cluster, project item locations in neural space and compare to spatial layout of behavioral task
* project items into 2D PCA space, extract X and Y coordinates (neural space)
```
extract_pc_embedding.py
```
see (link)[]

### 4) assess correlation between neural space and task space to quantify distance-based coding/compressed cognitive mapping
* for each run within each subject, create distance matrix for how far each target item is from each other target item within the spatial environment
* create distance matrix with identical comparisons for distances between target items in neural space (hippocampal representations)
see (pca_analyses_jupyter)[]
  
* correlate matrices to assess distance-based coding, compare to age group and performance
see (pca_analyses_R)[]


