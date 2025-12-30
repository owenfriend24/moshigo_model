### Grid-like coding in entorhinal cortex
* to test for grid-like coding of spatial locations (six-fold representational symmetry), we use an adapted multivariate similarity approach ([Bellmund et al., 2016](https://elifesciences.org/articles/17089))
* To summarize:
  1) extract neural activity from the initial navigation phase of each trial (first 3 TRs/6.0 seconds)
  2) residualize data (implement GLM with nuisance regressors as explanatory variables, extract residuals as clean 'task-related' activity)
  3) iteratively sweep searchlight sphere across the brain to identify voxels demonstrating grid-like activity (pairs of trials with angular difference of 60 deg. more similar than paris of trials with angular difference of 30 deg.)

### 1. extract residuals and necessary metadata from initial navigation phase of each trial
* to capture neural activity associated with navigation, take the first three TRs (6 seconds) of navigation from the spawn location
* high pass filter functional data at 128 Hz
* residualize data via GLM, treating motion regressors as explanatory variables and extracting residuals
  * resulting data should then have motion/image quality parameters regressed out
* for all trial pairs, extract angle between target locations to identify trials that either display six-fold symmetry (within 5 deg. of a multiple of 60 deg.) or not (within 5 deg. of a multiple of 30 deg., excluding 60 deg. pairs)
* write out ordered 4D neural data and metadata for searchlight similarity comparisons

```
prep_grid_data.py $subject $condition
```
see [link](https://github.com/owenfriend24/moshigo_model/blob/main/bin/prep_grid_data.py)

### 2. run searchlight to identify regions demonstrating grid-like activity
* using organized neural data and metadata above, compute similarity of aligned trials vs misaligned trials within each searchlight sphere
* implement 1000 permutation tests to compare difference between aligned trials and misaligned trials to a shuffled null
* can be split by proximal (cone) and distal (mountain) conditions if necessary

```
moshi_sl_grid.py $subject $condition $mask
```
see [main implementation](https://github.com/owenfriend24/moshigo_model/blob/main/bin/moshi_sl_grid.py) and [similarity function](https://github.com/owenfriend24/moshigo_model/blob/main/bin/grid_function_modulo60.py)

### 3. use permutation testing to identify regions in which grid-like activity varies parametrically with age; cluster correct resulting cluster
* before implementing Randomise, mask and smooth z-maps with 4mm kernel
```
grid_randomise.sh
```

### 4. reverse-normalize identified ERC cluster to each subject's native space
```
pull_grid_sim_values.py $subject
```

### 5. relate subject-level differences in grid-like coding to age and task performance
* see [link](https://github.com/owenfriend24/moshigo_model/blob/main/R_mds/grid_analyses.md) for manuscript analyses

<img width="2207" height="2316" alt="grid_figure_draft" src="https://github.com/user-attachments/assets/23b6eb7a-9fce-4bdd-87d5-1e5691c1c4b7" />

