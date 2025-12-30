### Compression of spatial information into low-dimensional cognitive maps

* to identify regions which compress spatial information across the task (and which do so differently by age group), we use voxelwise mixed-effects regression (Mack et al., 2020)
* to summarize:
   1) for item-level representations within each subject, we iteratively sweep a searchlight sphere across the brain, perform PCA, and exteract the % of variance explained by the top 2 principal components
   2) after transforming resulting variance maps into template space, we again iteratively sweet across the brain and implement a mixed-effects model with terms for age group, run, their interaction, and overall task performance, along with subject-level random intercept terms. 
   3) from the above comparison, we compute (1-p) maps to identify contiguous clusters in which we find an age group by run interaction
   4) finally, we back-project the corrected cluster from above (in the hippocampal tail) into each subject's native space to extract changes in variance and similarity between items
   
* this requires several millions of comparisons and must be implemented in parallel in high-performance computing (HPC) environment
* the below mixed-effects model is confirmatory, illustrating an age-by-run interaction within the hippocampal cluster identified via voxelwise mixed-effects regression
  * for voxelwise PCA searchlight, see associated Python files for implementation in HPC environments
  
