"""Dissimilarity measure"""

__docformat__ = 'restructuredtext'

import numpy as np
from numpy import *
from numpy.random import randint
import scipy.stats
from scipy.stats.mstats import zscore
from scipy.ndimage import convolve1d
from scipy.sparse import spdiags
from scipy.linalg import toeplitz
from mvpa2.measures.base import Measure
from mvpa2.measures import rsa
from sklearn.decomposition import PCA


class searchlight_function_pca(Measure):
    def __init__(self, n_components=3):
        Measure.__init__(self)
        self.n_components = n_components

    def __call__(self, dataset):
        """
        dataset: PyMVPA dataset. Expected shape = (4, voxels) for 4 items in the sphere.
        Returns:
            Sum of variance explained by top n_components.
        """
        # Defensive check: we expect 4 samples (items)
        if dataset.nsamples < self.n_components:
            return np.nan

        # Shape: samples (items) × features (voxels in sphere)
        data = dataset.samples

        if np.any(np.isnan(data)) or np.all(data == 0):
            return np.nan

        try:
            pca = PCA(n_components=self.n_components)
            pca.fit(data)
            var_expl = np.sum(pca.explained_variance_ratio_)
        except:
            var_expl = np.nan

        return var_expl
