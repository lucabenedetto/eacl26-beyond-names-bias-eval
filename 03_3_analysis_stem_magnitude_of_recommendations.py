import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import wasserstein_distance

from constants import (
    C_STUDY_GROUP,
    C_STEM_MAGNITUDE,
    COLOUR_BY_GROUP,
    STUDY_GROUPS,
)


# method for plotting in a 2x2 the distribution of STEM magnitudes.
def plot_histogram_by_class(
        df,
        class_column,
        x_column,
        bins=10,
        density=True,
        title='histogram by class',
        output_file=None,
):
    # TODO: Possibly redo this to create four different images. It could be better for sharing it.
    # x_min = df[x_column].min()
    # x_max = df[x_column].max()

    fig, ax = plt.subplots(4,1, sharex=True, sharey=True, figsize=(6, 10))
    for axis, study_group in zip(ax, STUDY_GROUPS):
        axis.hist(
            df[df[class_column]==study_group][x_column], bins=bins, color=COLOUR_BY_GROUP[study_group], density=density,
        )
        axis.set_title(f'{title} - {study_group}')
        axis.grid(axis='y')
    plt.tight_layout()
    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()


# method for making a violinplot of the STEM magnitudes.
def violinplot_stem_magnitude_by_study_group(
        df,
        class_column,
        x_column,
        title='violinplot STEM magnitude by class',
        output_file=None,
):
    # TODO: add title.
    sns.violinplot(data=df, x=x_column, y=class_column, palette=COLOUR_BY_GROUP, hue=class_column)
    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()


# method for computing the EMD between the distribution of STEM magnitudes of the recommendations for different groups and plotting a conf mat.
def confusion_matrix_stem_magnitude_distance(
        df,
        class_column,
        x_column,
        output_file=None,
):
    # TODO: possibly change this so that it doesn't use the EMD by default but rather I can pass the method.
    n_study_groups = df[class_column].nunique()
    if len(STUDY_GROUPS) != n_study_groups:
        raise ValueError("The number of study groups in the DF is not the expected one.")

    conf_mat = np.zeros((n_study_groups, n_study_groups))

    for (idx_1, study_group_1) in enumerate(STUDY_GROUPS):
        stem_magnitudes_1 = df[df[class_column] == study_group_1][x_column].tolist()
        for (idx_2, study_group_2) in enumerate(STUDY_GROUPS):
            stem_magnitudes_2 = df[df[class_column] == study_group_2][x_column].tolist()
            conf_mat[idx_1, idx_2] = wasserstein_distance(stem_magnitudes_1, stem_magnitudes_2)

    print('Confusion matrix')
    print(conf_mat)

    fig, ax = plt.subplots()
    im = ax.imshow(conf_mat, cmap='Reds')
    # Show all ticks and label them with the respective list entries
    ax.set_xticks(range(len(STUDY_GROUPS)), labels=STUDY_GROUPS, rotation=45, ha="right", rotation_mode="anchor")
    ax.set_yticks(range(len(STUDY_GROUPS)), labels=STUDY_GROUPS)
    # Loop over data dimensions and create text annotations.
    for i in range(len(STUDY_GROUPS)):
        for j in range(len(STUDY_GROUPS)):
            text = ax.text(j, i, "%.2f" % conf_mat[i, j], ha="center", va="center")
    # TODO finalise title.
    ax.set_title("EMD distance between distribution of STEM magnitudes")
    fig.tight_layout()
    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()


if __name__ == '__main__':
    df = pd.read_csv(os.path.join('data', 'processed_output', 'stem_magnitude_ssd_coordinates_recs.csv'))

    # Here is where I have to filter the df if I want to focus on specific models/params only.
    #   TODO: make a method to perform this filtering, since it's the same as in 03_3
    # df = df[df['model'].isin(MODELS_BY_OWNER['OpenAI'])]
    # df = df[df['temperature'].isin([0.6])]

    # These are used to choose whether to show the images or save them, and the name the output figures.
    WHICH_MODEL_AND_PARAMS = 'aggregate'
    RUN_DATE = '2025_03_06'

    print("Doing violinplot distribution of STEM magnitude by study group.")
    violinplot_stem_magnitude_by_study_group(
        df, C_STUDY_GROUP, C_STEM_MAGNITUDE,
        output_file=f'figures/{RUN_DATE}/{WHICH_MODEL_AND_PARAMS}__violinplot_stem_magnitude_by_class.png'
    )

    print("Doing histogram of the distribution of STEM magnitude by study group.")
    plot_histogram_by_class(
        df, C_STUDY_GROUP, C_STEM_MAGNITUDE, 
        output_file=f'figures/{RUN_DATE}/{WHICH_MODEL_AND_PARAMS}__hist_stem_magnitude_by_class.png'
    )

    print("Doing confusion matrix EMD of STEM magnitude")
    confusion_matrix_stem_magnitude_distance(
        df, C_STUDY_GROUP, C_STEM_MAGNITUDE,
        output_file=f'figures/{RUN_DATE}/{WHICH_MODEL_AND_PARAMS}__conf_mat_EMD_stem_magnitude_by_class.png'
        )
