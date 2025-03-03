import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns

from constants import (
    C_STUDY_GROUP, C_PCA_0, C_PCA_1, C_RECS,
    COLOUR_BY_GROUP,
    PALETTES_BY_GROUP,
    STUDY_GROUPS,
    MODELS_BY_OWNER,
)

def get_pca_coordinates_by_study_group(df, study_group):
    return np.array([(x1, x2) for x1, x2 in df[df[C_STUDY_GROUP] == study_group][[C_PCA_0, C_PCA_1]].values])


def scatter_plot_with_marginal_hist_plt(
        df_with_2d_coordinates,
        title='scatter plot with marginal histograms',
        output_file=None,
) -> None:
    """
    Generate a scatter plot with marginal histograms for the given coordinates grouped by type.
    """
    coordinates = {sg: get_pca_coordinates_by_study_group(df_with_2d_coordinates, sg) for sg in STUDY_GROUPS}

    fig = plt.figure(figsize=(10, 10))
    gs = fig.add_gridspec(3, 3)
    # Create the scatter plot
    ax_scatter = fig.add_subplot(gs[1:, :-1])
    for key, value in coordinates.items():
        ax_scatter.scatter([x[0] for x in value], [x[1] for x in value], label=key, alpha=0.5, color=COLOUR_BY_GROUP[key])
    ax_scatter.legend()
    ax_scatter.grid(True)
    # Create the x-axis histograms
    ax_histx = fig.add_subplot(gs[0, :-1])
    for key, value in coordinates.items():
        ax_histx.hist([x[0] for x in value], bins=30, alpha=0.5, color=COLOUR_BY_GROUP[key])
    ax_histx.set_xticks([])
    # Create the y-axis histograms
    ax_histy = fig.add_subplot(gs[1:, -1])
    for key, value in coordinates.items():
        ax_histy.hist([x[1] for x in value], bins=30, orientation='horizontal', alpha=0.5, color=COLOUR_BY_GROUP[key])
    ax_histy.set_yticks([])

    # Add a title
    plt.suptitle(title)  # , y=0.95)
    plt.tight_layout()
    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()


# TODO fix params
def scatter_plot_with_marginal_distributions_sns(
        df_with_2d_coordinates,
        title='scatter plot with marginal distributions (seaborn)',
        output_file=None,
):
    sns.jointplot(data=df_with_2d_coordinates, x=C_PCA_0, y=C_PCA_1, hue=C_STUDY_GROUP, palette=COLOUR_BY_GROUP)
    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()


# This was a first test to see the jointplot, but it looks a bit unreadable if I put everything in a single figure.
# def joint_plot_sns(
#         df_with_2d_coordinates,
#         title='jointplot (seaborn)',
#         output_file=None,
# ):
#     sns.jointplot(
#         data=df_with_2d_coordinates, x=C_PCA_0, y=C_PCA_1, hue=C_STUDY_GROUP, kind='kde', fill=True,
#         joint_kws={'alpha': 0.7}
#     )
#     if output_file:
#         plt.savefig(output_file)
#     else:
#         plt.show()


# TODO fix x & y lim
def joint_plot_by_class(
        df,
        class_column,
        x_column,
        y_column,
        title='joint plot by class',
        output_file=None,
):
    x_min, x_max, y_min, y_max = get_x_y_min_max(df)
    for study_group in ['model', 'f', 'm', 'x']:
        sns.jointplot(
            data=df[df[C_STUDY_GROUP]==study_group],
            x=x_column,
            y=y_column,
            hue=class_column,
            kind='kde',
            fill=True,
            palette=PALETTES_BY_GROUP[study_group],
            joint_kws={'alpha': 0.7},
            xlim=(x_min-2, x_max+2), ylim=(y_min-2, y_max+2),
        )
        if output_file:
            new_output_file = output_file.replace('.png', f'_{study_group}.png') # TODO change this to work with pdf too
            plt.savefig(new_output_file)
        else:
            plt.show()


def plot_hexbin_by_class(
        df,
        class_column,
        x_column,
        y_column,
        gridsize=16,
        title='hexbin by class',
        output_file=None,
):
    # TODO: Possibly redo this to create four different images. It could be better for sharing it.
    x_min, x_max, y_min, y_max = get_x_y_min_max(df)

    fig, ax = plt.subplots(2,2, sharex=True, sharey=True)
    for axis, study_group in zip([ax[0][0], ax[0][1], ax[1][0], ax[1][1]], STUDY_GROUPS):
        hb = axis.hexbin(
            df[df[class_column]==study_group][x_column], df[df[class_column]==study_group][y_column],
            bins='log', gridsize=gridsize, cmap=PALETTES_BY_GROUP[study_group], extent=(x_min, x_max, y_min, y_max)
        )
        cb = fig.colorbar(hb, ax=axis, label='counts')
        axis.set_title(f'{title} - {study_group}')
    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()


def get_x_y_min_max(df_with_2d_coordinates):
    # TODO make this using some x_column and y_column params instead of C_PCA_0 and C_PCA_1
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
    # df_2d_coord must be a dataframe with at least cols pca_0, pca_1, and recs
    # TODO: change this so that it works on different column names
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
    # df_2d_coord must be a dataframe with at least cols pca_0, pca_1, and recs
    # TODO: change this so that it works on different column names
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
    df = pd.read_csv(os.path.join('data', 'processed_output', f'pca_reduced_ssd_coordinates_aggregate.csv'))

    # Here is where I have to filter the df if I want to focus on specific models/params only.
    # df = df[df['model'].isin(MODELS_BY_OWNER['OpenAI'])]
    # df = df[df['temperature'].isin([0.6])]

    # These are used to choose whether to show the images or save them, and the name the output figures.
    WHICH_PCA = 'agg_pca'
    WHICH_MODEL_AND_PARAMS = 'aggregate'
    OUTPUT_FOLDER = os.path.join('figures', '2025_02_17')

    print("scatter_plot_with_marginal_hist_plt")
    scatter_plot_with_marginal_hist_plt(
        df,
        output_file=os.path.join(OUTPUT_FOLDER, f'{WHICH_PCA}__{WHICH_MODEL_AND_PARAMS}__scatter_with_marginals.png'),
    )
    # print_recommendations_from_corners(df, n_bins=5)
    # print_recommendations_from_borders(df, n_bins=15)

    print("scatter_plot_with_marginal_distributions_sns")
    scatter_plot_with_marginal_distributions_sns(
        df,
        output_file=os.path.join(OUTPUT_FOLDER, f'{WHICH_PCA}__{WHICH_MODEL_AND_PARAMS}__scatter_with_marginals_sns.png'),
    )

    # This will not be used in the analysis as it is not very readable.
    # print("joint_plot_sns")
    # joint_plot_sns(
    #     df,
    #     output_file=os.path.join(OUTPUT_FOLDER, f'{WHICH_PCA}__{WHICH_MODEL_AND_PARAMS}__joint_plot_sns.png'),
    # )

    print("plot_hexbin_by_class")
    plot_hexbin_by_class(
        df,
        C_STUDY_GROUP,
        C_PCA_0,
        C_PCA_1,
        output_file=os.path.join(OUTPUT_FOLDER, f'{WHICH_PCA}__{WHICH_MODEL_AND_PARAMS}__hexbin_by_class.png'),
    )

    print("joint_plot_by_class")
    joint_plot_by_class(
        df,
        C_STUDY_GROUP,
        C_PCA_0,
        C_PCA_1,
        output_file=os.path.join(OUTPUT_FOLDER, f'{WHICH_PCA}__{WHICH_MODEL_AND_PARAMS}__joint_plot_by_class.png'),
    )


if __name__ == '__main__':
    main()
