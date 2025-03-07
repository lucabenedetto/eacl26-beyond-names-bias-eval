import pandas as pd
import os
from scipy.stats import wasserstein_distance

if __name__ == '__main__':
    # this is to analyse the max possible EMD in our experimental settings.
    # It is basically computed by measuring the distance between two distributions which are made one of points at xmin, ymin and the other of points at xmax, ymax.
    df = pd.read_csv(os.path.join('data', 'processed_output', f'pca_reduced_ssd_coordinates_aggregate.csv'))

    x_min = df['pca_0'].min()
    x_max = df['pca_0'].max()
    y_min = df['pca_1'].min()
    y_max = df['pca_1'].max()
    
    distribution_1_pca_0 = [x_min] * 100  # Results were the same with 10 and 1000 (even when 100 for distribution 1 and 1000 for distribution 2).
    distribution_1_pca_1 = [y_min] * 100

    distribution_2_pca_0 = [x_max] * 100
    distribution_2_pca_1 = [y_max] * 100

    print("'MAX' EMD PCA_0 = %.2f" % wasserstein_distance(distribution_1_pca_0, distribution_2_pca_0))    
    print("'MAX' EMD PCA_1 = %.2f" % wasserstein_distance(distribution_1_pca_1, distribution_2_pca_1))    
    # 'MAX' EMD PCA_0 = 12.24 (on the ssd coordinates reduced with the aggregate PCA)
    # 'MAX' EMD PCA_1 = 8.90
