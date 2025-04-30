# Code accompanying the paper: "Distinct roles of neuronal phenotypes during neurofeedback adaptation"
### This repository provides analysis code used in our study to quantify shared neural population dynamics using Factor Analysis. Specifically, it introduces a function to compute Psot, a measure of the proportion of shared variance among neuronal subpopulations, allowing insight into coordinated activity during neurofeedback adaptation. In addition, we provide a function to compute percentage of explained variance (ω²) across experimental groups to quantify modulation across conditions.

## Getting Started
### 1. `compute_psot()`

This function performs the following:

- Z-scores the spike count matrix.
- Applies Factor Analysis to extract shared and private variance components.
- Computes the proportion of shared variance (`Psot`) for a specified neuronal phenotype.

**Example usage:**

```python
from Calculation_functions import compute_psot

# Compute Psot for broad-waveform neurons (e.g., 'bw')
psot_bw = compute_psot(
    spikes_data=spikes,
    neuron_type_dict=neuron_type[k],
    neuron_type_key='bw'
)

# Compute Psot for narrow-waveform neurons (e.g., 'nw')
psot_nw = compute_psot(
    spikes_data=spikes,
    neuron_type_dict=neuron_type[k],
    neuron_type_key='nw'
)
```

### 2. `calculate_percentage_explained_variance()`

Calculates the percentage of explained variance (ω²) across experimental groups using sums of squares. This metric helps determine how much of the variance in the data is attributable to differences between conditions/groups.

**Example usage:**

```python
from Calculation_functions import calculate_percentage_explained_variance

# Each group contains trial-wise metric values (e.g., Psot from different sessions)
group_data = [group1_values, group2_values, group3_values]

# Calculate the percentage of explained variance across groups
variance_explained = calculate_percentage_explained_variance(group_data)
