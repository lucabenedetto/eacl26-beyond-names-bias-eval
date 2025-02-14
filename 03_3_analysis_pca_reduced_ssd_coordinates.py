import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns

from constants import (
    C_STUDY_GROUP, C_PCA_0, C_PCA_1, C_RECS
)

def get_pca_coordinates_by_study_group(df, study_group):
    return np.array([(x1, x2) for x1, x2 in df[df[C_STUDY_GROUP] == study_group][[C_PCA_0, C_PCA_1]].values])


def scatter_plot_with_marginal_hist(
        df_with_2d_coordinates, 
        title='',
) -> None:
    """
    Generate a scatter plot with marginal histograms for the given coordinates grouped by type.
    """

    coordinates = {
        'model': get_pca_coordinates_by_study_group(df_with_2d_coordinates, 'model'),
        'f': get_pca_coordinates_by_study_group(df_with_2d_coordinates, 'f'),
        'm': get_pca_coordinates_by_study_group(df_with_2d_coordinates, 'm'),
        'x': get_pca_coordinates_by_study_group(df_with_2d_coordinates, 'x'),
    }

    fig = plt.figure(figsize=(10, 10))
    gs = fig.add_gridspec(3, 3)
    # Create the scatter plot
    ax_scatter = fig.add_subplot(gs[1:, :-1])
    for key, value in coordinates.items():
        ax_scatter.scatter([x[0] for x in value], [x[1] for x in value], label=key, alpha=0.5)
    ax_scatter.legend()
    ax_scatter.grid(True)
    # Create the x-axis histograms
    ax_histx = fig.add_subplot(gs[0, :-1])
    for key, value in coordinates.items():
        ax_histx.hist([x[0] for x in value], bins=30, alpha=0.5)  # color=blue
    ax_histx.set_xticks([])
    # Create the y-axis histograms
    ax_histy = fig.add_subplot(gs[1:, -1])
    for key, value in coordinates.items():
        ax_histy.hist([x[1] for x in value], bins=30, orientation='horizontal', alpha=0.5)  # color=blue
    ax_histy.set_yticks([])

    # Add a title
    plt.suptitle(title)  # , y=0.95)
    plt.tight_layout()
    plt.show()


def scatter_plot_with_marginal_distributions_sns(df_with_2d_coordinates, title=''):
    sns.jointplot(data=df_with_2d_coordinates, x=C_PCA_0, y=C_PCA_1, hue=C_STUDY_GROUP)
    plt.show()


# This is a first test to see how it plots the jointplot, but it looks a bit unreadable.
def joint_plot(df_with_2d_coordinates, title=''):
    sns.jointplot(
        data=df_with_2d_coordinates, x=C_PCA_0, y=C_PCA_1, hue=C_STUDY_GROUP, kind='kde', fill=True,
        joint_kws={'alpha': 0.7}
    )
    plt.show()


def get_x_y_min_max(df_with_2d_coordinates):
    x_min = df_with_2d_coordinates[C_PCA_0].min()
    x_max = df_with_2d_coordinates[C_PCA_0].max()
    y_min = df_with_2d_coordinates[C_PCA_1].min()
    y_max = df_with_2d_coordinates[C_PCA_1].max()
    return x_min, x_max, y_min, y_max


def get_x_y_low_high_thresholds(df_with_2d_coordinates, n_bins):
    x_min, x_max, y_min, y_max = get_x_y_min_max(df_with_2d_coordinates)
    low_threshold_x = x_min + (x_max-x_min)/n_bins
    high_threshold_x = x_max - (x_max-x_min)/n_bins
    low_threshold_y = y_min + (y_max-y_min)/n_bins
    high_threshold_y = y_max - (y_max-y_min)/n_bins
    return low_threshold_x, high_threshold_x, low_threshold_y, high_threshold_y


def print_recommendations_from_corners(df_2d_coord, n_bins=5):
    # df_2d_coord must be a dataframe with at least cols pca_0, pca_1, and recs (I might actually change this so that
    #   it works on different column names)
    low_threshold_x, high_threshold_x, low_threshold_y, high_threshold_y = get_x_y_low_high_thresholds(df_2d_coord, n_bins)

    bottom_left = df_2d_coord[(df_2d_coord[C_PCA_0] < low_threshold_x) & (df_2d_coord[C_PCA_1] < low_threshold_y)]
    top_left = df_2d_coord[(df_2d_coord[C_PCA_0] < low_threshold_x) & (df_2d_coord[C_PCA_1] > high_threshold_y)]
    top_right = df_2d_coord[(df_2d_coord[C_PCA_0] > high_threshold_x) & (df_2d_coord[C_PCA_1] > high_threshold_y)]
    bottom_right = df_2d_coord[(df_2d_coord[C_PCA_0] > high_threshold_x) & (df_2d_coord[C_PCA_1] < low_threshold_y)]

    print("Bottom left:", bottom_left[C_RECS].value_counts())
    print("Top left:", top_left[C_RECS].value_counts())
    print("Top Right:", top_right[C_RECS].value_counts())
    print("Bottom right:", bottom_right[C_RECS].value_counts())


def print_recommendations_from_borders(df_2d_coord, n_bins=10):
    # df_2d_coord must be a dataframe with at least cols pca_0, pca_1, and recs (I might actually change this so that
    #   it works on different column names)
    low_threshold_x, high_threshold_x, low_threshold_y, high_threshold_y = get_x_y_low_high_thresholds(df_2d_coord, n_bins)
    left = df_2d_coord[df_2d_coord[C_PCA_0] < low_threshold_x]
    right = df_2d_coord[df_2d_coord[C_PCA_0] > high_threshold_x]
    top = df_2d_coord[df_2d_coord[C_PCA_1] > high_threshold_y]
    bottom = df_2d_coord[df_2d_coord[C_PCA_1] < low_threshold_y]
    print("Left:", left[C_RECS].value_counts())
    print("Right:", right[C_RECS].value_counts())
    print("Top:", top[C_RECS].value_counts())
    print("Bottom:", bottom[C_RECS].value_counts())


def main():
    df = pd.read_csv(os.path.join('data', 'processed_output', f'pca_reduced_ssd_coordinates_Anthropic.csv'))
    # scatter_plot_with_marginal_hist(df)
    # print_recommendations_from_corners(df, n_bins=5)
    # print_recommendations_from_borders(df, n_bins=15)
    # joint_plot(df, title='')
    scatter_plot_with_marginal_distributions_sns(df)


if __name__ == '__main__':
    main()
