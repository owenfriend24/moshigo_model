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
    def __init__(self, n_components=4):
        Measure.__init__(self)
        self.n_components = n_components

    def __call__(self, dataset):
        data = dataset.samples
        #print("X shape:", data.shape)
        #print("X variance per voxel:", np.var(data, axis=0)[:5])
        #print("Correlation matrix:")
        #print(np.round(np.corrcoef(data), 2))

        # # don't run if contains nans? or will pymvpa automatically deal with this?
        # if data.shape[1] < 10 or np.any(np.isnan(data)):
        #     return np.nan

        pca = PCA(n_components=self.n_components)
        pca.fit(data)
        #print("Explained variance:", pca.explained_variance_ratio_)
        return np.sum(pca.explained_variance_ratio_[:2])



