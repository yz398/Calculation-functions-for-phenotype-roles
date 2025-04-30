# -*- coding: utf-8 -*-
# function to calculate Factor analysis
import numpy as np
from sklearn.decomposition import FactorAnalysis
from sklearn.preprocessing import StandardScaler

def compute_psot(spikes_data, neuron_type_dict, neuron_type_key, n_components=6):
    """
    Computes Psot (proportion of shared variance) using Factor Analysis.

    Parameters:
    -----------
    spikes_data : ndarray
        2D array of spike counts (trials x neurons) or z-scored neural activity.
    
    neuron_type_dict : dict
        Dictionary with keys like 'bw' and 'nw' mapping to lists of neuron indices.
    
    neuron_type_key : str
        Key to select the type of neuron (e.g., 'bw' for behaviorally relevant neurons).
    
    n_components : int
        Number of latent dimensions to extract using Factor Analysis.

    Returns:
    --------
    pshared : float
        Proportion of variance that is shared for the selected neuron type.
    """
    # Z-score the data
    z_spikes = StandardScaler().fit_transform(spikes_data)

    # Perform Factor Analysis
    fa = FactorAnalysis(n_components=n_components)
    fa.fit(z_spikes)

    # Decompose shared and private variances
    shared = np.dot(fa.components_.T, fa.components_)
    private = np.diag(fa.noise_variance_)

    # Compute total variance
    total = np.trace(shared + private)

    # Select neurons of the given type
    neuron_indices = neuron_type_dict[neuron_type_key]

    # Compute shared variance trace for those neurons
    shared_sum = np.sum(shared[np.ix_(neuron_indices, neuron_indices)])

    # Normalize by total variance and number of neurons
    pshared = shared_sum / (total * len(neuron_indices))

    return pshared


#%% function to calculate percentage_explained_variance
def calculate_percentage_explained_variance(group_data):
    """
    Calculate the percentage of explained variance (omega squared, ω²) and multiply by 100.
    
    Parameters:
    group_data (list of arrays): Each element is an array representing the data of one group.
    
    Returns:
    float: The percentage of explained variance.
    """
    # Number of groups
    G = len(group_data)
    
    # Calculate group means and overall mean
    n_group = np.array([len(group) for group in group_data])  # Number of trials per group
    x_bar_group = np.array([np.mean(group) for group in group_data])  # Mean activity per group
    x_bar = np.mean(np.concatenate(group_data))  # Overall mean
    
    # Calculate SS_BetweenGroups
    SS_between_groups = np.sum(n_group * (x_bar_group - x_bar) ** 2)
    
    # Calculate SS_Total
    #SS_total = np.sum([(x - x_bar) ** 2 for group in group_data for x in group]) original
    SS_total = np.sum((np.concatenate(group_data) - x_bar) ** 2)
    
    # Calculate MSE (Mean Squared Error)
    #MSE = np.sum([(x - x_bar_group[i]) ** 2 for i, group in enumerate(group_data) for x in group]) / (sum(n_group) - G)
    MSE = np.sum([np.sum((group - x_bar_group[i]) ** 2) for i, group in enumerate(group_data)]) / (sum(n_group) - G)
    
    # Degrees of freedom (df = G - 1)
    df = G - 1
    
    # Calculate omega squared and then multiply by 100 to get the percentage
    omega_squared_percentage = ((SS_between_groups - (df * MSE)) / (SS_total + MSE)) * 100
    
    return omega_squared_percentage