import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

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
    x_min = df[x_column].min()
    x_max = df[x_column].max()

    fig, ax = plt.subplots(2,2, sharex=True, sharey=True)
    for axis, study_group in zip([ax[0][0], ax[0][1], ax[1][0], ax[1][1]], STUDY_GROUPS):
        axis.hist(
            df[df[class_column]==study_group][x_column], bins=bins, color=COLOUR_BY_GROUP[study_group], density=density,
        )
        axis.set_title(f'{title} - {study_group}')
        axis.grid(axis='y')
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
    # TODO: title and save file.
    sns.violinplot(data=df, x=x_column, y=class_column, palette=COLOUR_BY_GROUP)
    plt.show()


# method for computing the EMD between the distribution of STEM magnitudes of the recommendations for different groups and plotting a conf mat.


if __name__ == '__main__':
    df = pd.read_csv(os.path.join('data', 'processed_output', 'stem_magnitude_ssd_coordinates_recs.csv'))

    # Here is where I have to filter the df if I want to focus on specific models/params only.
    #   TODO: make a method to perform this filtering, since it's the same as in 03_3
    # df = df[df['model'].isin(MODELS_BY_OWNER['OpenAI'])]
    # df = df[df['temperature'].isin([0.6])]

    # These are used to choose whether to show the images or save them, and the name the output figures.
    WHICH_PCA = 'agg_pca'
    WHICH_MODEL_AND_PARAMS = 'aggregate'
    OUTPUT_FOLDER = os.path.join('figures', '2025_02_17')

    print("Doing violinplot distribution of STEM magnitude by study group.")
    violinplot_stem_magnitude_by_study_group(df, C_STUDY_GROUP, C_STEM_MAGNITUDE)

    print("Doing histogram of the distribution of STEM magnitude by study group.")
    plot_histogram_by_class(df, C_STUDY_GROUP, C_STEM_MAGNITUDE)

    print(df.columns)

    pass
