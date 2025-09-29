import pandas as pd
import os
from scipy.stats import wasserstein_distance

from constants import (
    C_STEM_MAGNITUDE,
    C_PCA_0,
    C_PCA_1,
    CONFIG_NO_NAME,
    CONFIG_W_NAMES,
    CONFIG_AGGREGATE,
)


if __name__ == '__main__':
    # this is to analyse the max possible EMD in our experimental settings.
    # It is basically computed by measuring the distance between two distributions which are made one of points at xmin, ymin and the other of points at xmax, ymax.
    df = pd.read_csv(os.path.join('data', 'processed_output', f'pca_reduced_ssd_coordinates_aggregate.csv'))

    for prompt_param in [CONFIG_NO_NAME, CONFIG_W_NAMES, CONFIG_AGGREGATE]:
        if prompt_param in [CONFIG_NO_NAME, CONFIG_W_NAMES]:
            local_df = df[df['prompt_param'] == prompt_param]
        elif prompt_param == CONFIG_AGGREGATE:
            local_df = df
        else:
            raise ValueError(f"Unknown prompt param {prompt_param}.")

        print(f"Running prompt_param {prompt_param}.")
        x_min = local_df[C_PCA_0].min()
        x_max = local_df[C_PCA_0].max()
        y_min = local_df[C_PCA_1].min()
        y_max = local_df[C_PCA_1].max()

        distribution_1_pca_0 = [x_min] * 100  # Results were the same with 10 and 1000 (even when 100 for distribution 1 and 1000 for distribution 2).
        distribution_1_pca_1 = [y_min] * 100

        distribution_2_pca_0 = [x_max] * 100
        distribution_2_pca_1 = [y_max] * 100

        print("'MAX' EMD PCA_0 = %.2f" % wasserstein_distance(distribution_1_pca_0, distribution_2_pca_0))
        print("'MAX' EMD PCA_1 = %.2f" % wasserstein_distance(distribution_1_pca_1, distribution_2_pca_1))
        # 'MAX' EMD PCA_0 = 14.83 (on the ssd coordinates reduced with the aggregate PCA)
        # 'MAX' EMD PCA_1 = 11.03

    print("- - - - -")

    df = pd.read_csv(os.path.join('data', 'processed_output', 'stem_magnitude_ssd_coordinates_recs.csv'))
    for prompt_param in [CONFIG_NO_NAME, CONFIG_W_NAMES, CONFIG_AGGREGATE]:
        if prompt_param in [CONFIG_NO_NAME, CONFIG_W_NAMES]:
            local_df = df[df['prompt_param'] == prompt_param]
        elif prompt_param == CONFIG_AGGREGATE:
            local_df = df
        else:
            raise ValueError(f"Unknown prompt param {prompt_param}.")

        print(f"Running prompt_param {prompt_param}.")
        distribution_1 = [local_df[C_STEM_MAGNITUDE].min()] * 100
        distribution_2 = [local_df[C_STEM_MAGNITUDE].max()] * 100
        print("'MAX' EMD STEM magnitude = %.2f" % wasserstein_distance(distribution_1, distribution_2))

# Run for the October version of the paper
# Running prompt_param no_name.
# 'MAX' EMD PCA_0 = 14.36
# 'MAX' EMD PCA_1 = 9.66
# - - - - -
# Running prompt_param with_names.
# 'MAX' EMD PCA_0 = 14.83
# 'MAX' EMD PCA_1 = 11.03
# - - - - -
# Running prompt_param aggregate.
# 'MAX' EMD PCA_0 = 14.83
# 'MAX' EMD PCA_1 = 11.03
# - - - - -
# Running prompt_param no_name.
# 'MAX' EMD STEM magnitude = 15.00
# Running prompt_param with_names.
# 'MAX' EMD STEM magnitude = 15.00
# Running prompt_param aggregate.
# 'MAX' EMD STEM magnitude = 15.00


# For the older experiments (paper version of May).
# On the experiments without names (aggregate PCA):
# 'MAX' EMD PCA_0 = 12.24 (on the ssd coordinates reduced with the aggregate PCA)
# 'MAX' EMD PCA_1 = 8.90
# On the experiments with names (aggregate PCA):
# 'MAX' EMD PCA_0 = 13.08
# 'MAX' EMD PCA_1 = 9.13
# On the experiments without names (aggregate PCA):
# 'MAX' EMD STEM magnitude = 15.00
# On the experiments with names (aggregate PCA):
# 'MAX' EMD STEM magnitude = 15.00
