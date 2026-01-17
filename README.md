# Low-dimensional cognitive maps and grid-like coding in the developing hippocampus
* aka moshiGO
---

### Highlights:
* Identified low-dimensional neural representations (“cognitive maps”) that predict spatial memory precision and generalization across development
* Applied large-scale unsupervised learning (PCA) to >100M neural datapoints to extract interpretable representational trajectories
* Linked neural representational geometry to behavioral performance using scalable mixed-effects modeling and non-parametric permutation testing
* Built a high-throughput, parallelized analysis pipeline (Slurm + Joblib) enabling >1.4M statistical models to run in hours instead of days
* Fully reproducible, HPC-ready analysis workflow

### Methods at a glance:
* Unsupervised dimensionality reduction (PCA) on high-dimensional fMRI representations
* Simulation-derived null models for time-series similarity analyses (A/B-testing style inference)
* Large-scale mixed-effects modeling (1.4M+ models) and parallel compute orchestration with Slurm and Joblib
---

<img width="2224" height="1430" alt="pca_approach_wpoints" src="https://github.com/user-attachments/assets/46688623-d6db-4f2b-aaba-421dd97391c4" />
<img width="2216" height="1396" alt="task_pc_space_fig" src="https://github.com/user-attachments/assets/5425d20b-814e-4bf1-8605-812b279ec9a0" />

---
### Repo description:
This repository details three primary sets of analyses reported in *Hippocampal development enhances spatial memory precision and generalization* ([preprint]()). The repository is organized into three modular analysis tracks, each aligned with a core modeling question:

Markdown files detail three primary sections:
1) PCA-based identification of low-dimensional cognitive maps in hippocampus, operating on >100M neural datapoints ([pca analyses](https://github.com/owenfriend24/moshigo_model/blob/main/README_pca_analyses.md))
2)Multivariate signatures of grid-like coding in entorhinal cortex, including simulation-derived null comparisons for geometric time-series structure ([grid analyses](https://github.com/owenfriend24/moshigo_model/blob/main/2_grid_analyses.md))
3) Age- and run-level differences in representational similarity and memory performance on spatial navigation task ([behavior and rsa analyses](https://github.com/owenfriend24/moshigo_model/blob/main/R_mds/full_maintext_results.md))
All analyses operate on subject-level, preprocessed fMRI representations and are designed for scalability and reproducibility on high-performance computing clusters.
---

### Project description:

While adults form detailed and flexible representations of locations and landmarks, children tend to form spatial knowledge that is less precise and less adaptable to new environments. The present study directly tests the neural representational mechanisms underlying these behavioral differences, capturing fMRI activity while children and adults complete a dynamic spatial navigation task that requires generalization beyond directly experienced trajectories.

A primary finding is that adults and high-performing adolescents form compressed, low-dimensional cognitive maps that progressively encode Euclidean distances between locations as learning unfolds (pictured below). These representations were identified using large-scale PCA, enabling the recovery of interpretable representational trajectories linked to individual differences in memory performance.

In contrast, children rely more heavily on discrete and rigid representational formats, supported by grid-like coding in entorhinal cortex, which limits spatial precision under environmental change. To rigorously quantify these differences, we employed simulation-derived null models for time-series similarity, enabling A/B-style comparisons of geometric coding across age groups.

By combining unsupervised representation learning, simulation-based inference, and massively parallel mixed-effects modeling, this project reveals fundamental differences in the neural representation of spatial memories across development.

---


Feel free to reach out to ofriend@utexas.edu with any questions!
