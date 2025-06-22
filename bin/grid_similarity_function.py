import numpy as np
from mvpa2.measures.base import Measure
from mvpa2.measures import rsa
import random
import pandas as pd

class grid_similarity_function(Measure):
    """
    Searchlight function to compare representational similarity
    between trial pairs with angular difference % 60 ≈ 0 vs. ≈ 30 (±5° tolerance),
    across runs only.
    """

    def __init__(self, metric="correlation", tolerance=5):
        super().__init__()
        self.metric = metric
        self.tolerance = tolerance

    def __call__(self, dataset):

        def is_modulo_match(remainder, target, tol):
            return min(abs(remainder - target), 60 - abs(remainder - target)) <= tol

        # Compute similarity matrix (Fisher z-transformed)
        dsm = rsa.PDist(square=True, pairwise_metric=self.metric, center_data=False)
        dsm_matrix = 1 - dsm(dataset).samples
        # dsm_matrix = np.clip(dsm_matrix, -0.999999, 0.999999)
        dsm_matrix = np.arctanh(dsm_matrix)

        # print(f"len dsm_matrix - {len(dsm_matrix)}")
        angles = dataset.sa['trial_angle']
        # print(f"trial angles: {angles}")
        runs = dataset.sa['run']
        n = len(dataset)

        sim_mod0 = []
        sim_mod30 = []
        # valid_angles = []
        data = pd.DataFrame(columns = ["comparison", "fisher_z"])

        for i in range(n):
            for j in range(i + 1, n):
                if runs[i] != runs[j]:
                    diff = abs(angles[i] - angles[j]) % 360
                    # print(f"diff between {angles[i]} - {angles[j]}; mod 360 = {diff}")
                    diff = min(diff, 360 - diff)  # wrap to [0, 180]
                    # print(f"wrapped diff: {diff}")
                    remainder = diff % 60
                    # print(f"remainder diff % 60 = {remainder}")

                    sim = dsm_matrix[i, j]

                    if is_modulo_match(remainder, 0, self.tolerance):
                        sim_mod0.append(sim)
                        data.loc[len(data)] = ['60_degree', sim]

                    elif is_modulo_match(remainder, 30, self.tolerance):
                        sim_mod30.append(sim)
                        data.loc[len(data)] = ['30_degree', sim]
        return data
