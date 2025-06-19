import numpy as np
from mvpa2.measures.base import Measure
from mvpa2.measures import rsa
import random

class grid_function_modulo60(Measure):
    """
    Searchlight function to compare representational similarity
    between trial pairs with angular difference % 60 ≈ 0 vs. ≈ 30 (±5° tolerance),
    across runs only.
    """

    def __init__(self, metric="correlation", niter=1000, tolerance=5):
        super().__init__()
        self.metric = metric
        self.niter = niter
        self.tolerance = tolerance

    def __call__(self, dataset):

        def is_modulo_match(remainder, target, tol):
            return min(abs(remainder - target), 60 - abs(remainder - target)) <= tol

        # Compute similarity matrix (Fisher z-transformed)
        dsm = rsa.PDist(square=True, pairwise_metric=self.metric, center_data=False)
        dsm_matrix = 1 - dsm(dataset).samples
        dsm_matrix = np.arctanh(dsm_matrix)
        print(f"len dsm_matrix - {len(dsm_matrix)}")
        angles = dataset.sa['trial_angle']
        print(f"trial angles: {angles}")
        runs = dataset.sa['run']
        n = len(dataset)

        sim_mod0 = []
        sim_mod30 = []

        for i in range(n):
            for j in range(i + 1, n):
                if runs[i] != runs[j]:
                    diff = abs(angles[i] - angles[j]) % 360
                    print(f"diff between {angles[i]} - {angles[j]}; mod 360 = {diff}")
                    diff = min(diff, 360 - diff)  # wrap to [0, 180]
                    print(f"wrapped diff: {diff}")
                    remainder = diff % 60
                    print(f"remainder diff % 60 = {remainder}")

                    sim = dsm_matrix[i, j]

                    if is_modulo_match(remainder, 0, self.tolerance):
                        sim_mod0.append(sim)
                        print(f"match for 0/60 condition")
                        print()
                        print()
                    elif is_modulo_match(remainder, 30, self.tolerance):
                        sim_mod30.append(sim)
                        print(f"match for 30 condition")
                        print()
                        print()

                    else:
                        print("no comparison conditions met")
                        print()
                        print()

        sim_mod0 = np.array(sim_mod0)
        sim_mod30 = np.array(sim_mod30)

        if len(sim_mod0) < 2 or len(sim_mod30) < 2:
            return np.nan

        obsstat = np.mean(sim_mod0) - np.mean(sim_mod30)

        # Permutation test
        combined = np.concatenate([sim_mod0, sim_mod30])
        n_mod0 = len(sim_mod0)
        randstat = []

        for _ in range(self.niter):
            np.random.shuffle(combined)
            rand_0 = combined[:n_mod0]
            rand_30 = combined[n_mod0:]
            randstat.append(np.mean(rand_0) - np.mean(rand_30))

        randstat = np.array(randstat)
        z_stat_60_ovr_30 = (obsstat - np.mean(randstat)) / np.std(randstat)
        z_stat_30_ovr_60 = - z_stat_60_ovr_30
        return z_stat_60_ovr_30, z_stat_30_ovr_60
