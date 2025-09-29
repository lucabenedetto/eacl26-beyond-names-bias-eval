import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns
from scipy.stats import wasserstein_distance

from constants import (
    C_STUDY_GROUP, C_PCA_0, C_PCA_1, C_RECS,
    COLOUR_BY_GROUP,
    PALETTES_BY_GROUP,
    STUDY_GROUPS,
    MODELS_BY_OWNER,
    MODELS_LIST,
    USER_AS_STUDENT, 
    LLM_AS_STUDENT,
    THIRD_PERSON_AS_STUDENT,
    CONFIG_NO_NAME,
    CONFIG_W_NAMES,
)


plt.rcParams.update({
    "font.size": 16,
    "font.family": "serif",
})


def get_pca_coordinates_by_study_group(df, study_group):
    return np.array([(x1, x2) for x1, x2 in df[df[C_STUDY_GROUP] == study_group][[C_PCA_0, C_PCA_1]].values])


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


# TODO fix params
def scatter_plot_with_marginal_distributions_sns(
        df_with_2d_coordinates,
        title='scatter plot with marginal distributions (seaborn)',
        output_file=None,
):
    sns.jointplot(data=df_with_2d_coordinates, x=C_PCA_0, y=C_PCA_1, hue=C_STUDY_GROUP, palette=COLOUR_BY_GROUP)
    if output_file:
        plt.savefig(output_file)
        plt.close()
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

    filtered_study_groups = [x for x in STUDY_GROUPS if x in df[class_column].unique()]

    # When I have all the study groups
    if len(filtered_study_groups) == 4:
        fig, ax = plt.subplots(2,2, sharex=True, sharey=True, figsize=(8, 7))
        for axis, study_group in zip([ax[0][0], ax[0][1], ax[1][0], ax[1][1]], STUDY_GROUPS):
            hb = axis.hexbin(
                df[df[class_column]==study_group][x_column], df[df[class_column]==study_group][y_column],
                bins='log', gridsize=gridsize, cmap=PALETTES_BY_GROUP[study_group], extent=(x_min, x_max, y_min, y_max),
            )
            cb = fig.colorbar(hb, ax=axis)  # , label='counts')
            axis.set_title(f'{study_group.title()}')
    # For when I have only two study groups (with names, F and M).
    elif len(filtered_study_groups) == 2:
        fig, ax = plt.subplots(1,2, sharex=True, sharey=True, figsize=(8, 4))
        for axis, study_group in zip([ax[0], ax[1]], filtered_study_groups):
            hb = axis.hexbin(
                df[df[class_column]==study_group][x_column], df[df[class_column]==study_group][y_column],
                bins='log', gridsize=gridsize, cmap=PALETTES_BY_GROUP[study_group], extent=(x_min, x_max, y_min, y_max)
            )
            # cb = fig.colorbar(hb, ax=axis, label='counts')  # TODO: fix this, it was causing an error.
            axis.set_title(f'{study_group.title()}')
    else:
        raise ValueError("Unsupported number of study groups.")
    if output_file:
        plt.savefig(output_file)
        plt.close()
    else:
        plt.show()


def confusion_matrix_distribution_distance(
        df,
        class_column,
        x_column,
        y_column,
        vmax=5,  # Selected this after doing a first analysis of all the results.
        # title='hexbin by class',
        output_file=None,
):
    # TODO: possibly change this so that it doesn't use the EMD by default but rather I can pass the method.

    # TODO: make a method for this, it is used in several scripts/methods.
    n_study_groups = df[class_column].nunique()
    if len(STUDY_GROUPS) != n_study_groups:
        print(f"[WARNING]T he number of study groups in the DF ({n_study_groups}) is not the expected one {len(STUDY_GROUPS)}.")

    # I am using this order instead of the original one in the constant STUDY_GROUPS because it better highlights the trends in the heatmaps.
    reordered_study_groups = ['model', 'm', 'x', 'f']
    reordered_study_groups = [x for x in reordered_study_groups if x in df[class_column].unique()]
    fig, ax = plt.subplots(1, 2, figsize=(8, 4))
    for ax_idx, column in enumerate([x_column, y_column]):
        conf_mat = np.zeros((n_study_groups, n_study_groups))

        for (idx_1, study_group_1) in enumerate(reordered_study_groups):
            stem_magnitudes_1 = df[df[class_column] == study_group_1][column].tolist()
            for (idx_2, study_group_2) in enumerate(reordered_study_groups):
                stem_magnitudes_2 = df[df[class_column] == study_group_2][column].tolist()
                conf_mat[idx_1, idx_2] = wasserstein_distance(stem_magnitudes_1, stem_magnitudes_2)

        im = ax[ax_idx].imshow(conf_mat, cmap='Reds', vmax=vmax)
        # Show all ticks and label them with the respective list entries
        ax[ax_idx].set_xticks(range(len(reordered_study_groups)), labels=[x.title() for x in reordered_study_groups])
        ax[ax_idx].set_yticks(range(len(reordered_study_groups)), labels=[x.title() for x in reordered_study_groups], rotation=90, va='center')
        # Loop over data dimensions and create text annotations.
        for i in range(len(reordered_study_groups)):
            for j in range(len(reordered_study_groups)):
                text = ax[ax_idx].text(j, i, "%.2f" % conf_mat[i, j], ha="center", va="center")
        ax[ax_idx].set_title(f"EMD ({column.upper().replace('_', ' ')})")
    fig.tight_layout()
    if output_file:
        plt.savefig(output_file)
        plt.close()
    else:
        plt.show()


def run_analysis_pca_reduced_ssd_coordinates(df, output_folder, which_pca, which_model_and_params):

    print("EMD between distribution of PCA reduced s.s.d. coordinates.")
    confusion_matrix_distribution_distance(
        df,
        C_STUDY_GROUP,
        C_PCA_0,
        C_PCA_1,
        output_file=os.path.join(output_folder, f'{which_pca}__{which_model_and_params}__conf_mat_EMD_ssd_coordinates.png'),
        )

    # Note 2025 05 13: I don't think we will use this in the paper in the end, but I am not removing it for the time being since it is more readable than the other.
    print("scatter_plot_with_marginal_distributions_sns")
    scatter_plot_with_marginal_distributions_sns(
        df,
        output_file=os.path.join(output_folder, f'{which_pca}__{which_model_and_params}__scatter_with_marginals_sns.png'),
    )

    print("plot_hexbin_by_class")
    plot_hexbin_by_class(
        df,
        C_STUDY_GROUP,
        C_PCA_0,
        C_PCA_1,
        output_file=os.path.join(output_folder, f'{which_pca}__{which_model_and_params}__hexbin_by_class.png'),
    )


def run_complete_analysis_pca_reduced_ssd_coordinates(df, WHICH_PCA, OUTPUT_FOLDER):

    # Create the folder if it doesn't exist
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        print(f"Folder '{OUTPUT_FOLDER}' created.")
    else:
        print(f"Folder '{OUTPUT_FOLDER}' already exists.")

    # Analysis aggregating all the models and runs.
    run_analysis_pca_reduced_ssd_coordinates(df, OUTPUT_FOLDER, WHICH_PCA, 'aggregate')

    # Analysis on separately on the different models
    for model_owner, list_models in MODELS_BY_OWNER.items():
        local_df = df[df['model'].isin(list_models)]
        run_analysis_pca_reduced_ssd_coordinates(local_df, OUTPUT_FOLDER, WHICH_PCA, model_owner)

    # Analysis on different temperature values
    for temperature in [0.0, 0.3, 0.6]:
        local_df = df[df['temperature'] == temperature]
        run_analysis_pca_reduced_ssd_coordinates(local_df, OUTPUT_FOLDER, WHICH_PCA, f'aggregate_temp_{temperature}')
    # for temperatures in [[0.0, 0.3], [0.3, 0.6]]:
    #     local_df = df[df['temperature'].isin(temperatures)]
    #     run_analysis_pca_reduced_ssd_coordinates(local_df, OUTPUT_FOLDER, WHICH_PCA, f'aggregate_temp_{temperatures[0]}_{temperatures[1]}')

    # analysis on different temperature values and different models
    for model_owner, list_models in MODELS_BY_OWNER.items():
        for temperature in [0.0, 0.3, 0.6]:
            local_df = df[df['model'].isin(list_models)]
            local_df = local_df[local_df['temperature'] == temperature]
            run_analysis_pca_reduced_ssd_coordinates(local_df, OUTPUT_FOLDER, WHICH_PCA, f'{model_owner}_temp_{temperature}')

    # analysis on the individual models
    for model in MODELS_LIST:
        local_df = df[df['model'] == model]
        run_analysis_pca_reduced_ssd_coordinates(local_df, OUTPUT_FOLDER, WHICH_PCA, model)

    # analysis on the different prompt types
    for prompt_type in [USER_AS_STUDENT, LLM_AS_STUDENT, THIRD_PERSON_AS_STUDENT]:
        local_df = df[df['prompt_type'] == prompt_type]
        run_analysis_pca_reduced_ssd_coordinates(local_df, OUTPUT_FOLDER, WHICH_PCA, f'aggregate_{prompt_type}')

    # analysis on the different prompt types and families of models
    for model_owner, list_models in MODELS_BY_OWNER.items():
        for prompt_type in [USER_AS_STUDENT, LLM_AS_STUDENT, THIRD_PERSON_AS_STUDENT]:
            local_df = df[df['model'].isin(list_models)]
            local_df = local_df[local_df['prompt_type'] == prompt_type]
            run_analysis_pca_reduced_ssd_coordinates(local_df, OUTPUT_FOLDER, WHICH_PCA, f'{model_owner}_{prompt_type}')


if __name__ == '__main__':
    df = pd.read_csv(os.path.join('data', 'processed_output', f'pca_reduced_ssd_coordinates_aggregate.csv'))

    WHICH_PCA = 'agg_pca'  # The PCA model to use. All results in the paper are the ones obtained using the aggragete model (trained on all provided recommendations).
    RUN_DATE = "2025_09_29_for_paper"

    print("Doing both with and without names")
    OUTPUT_FOLDER = os.path.join('figures', RUN_DATE, 'analysis_pca_reduced_ssd_aggregate')
    run_complete_analysis_pca_reduced_ssd_coordinates(df, WHICH_PCA, OUTPUT_FOLDER)

    print("Doing without names")
    OUTPUT_FOLDER = os.path.join('figures', RUN_DATE, 'analysis_pca_reduced_ssd_no_names')
    run_complete_analysis_pca_reduced_ssd_coordinates(df[df['prompt_param'] == CONFIG_NO_NAME], WHICH_PCA, OUTPUT_FOLDER)

    print("Doing with names")
    OUTPUT_FOLDER = os.path.join('figures', RUN_DATE, 'analysis_pca_reduced_ssd_with_names')
    run_complete_analysis_pca_reduced_ssd_coordinates(df[df['prompt_param'] == CONFIG_W_NAMES], WHICH_PCA, OUTPUT_FOLDER)


    # To run single analyses.
    # WHICH_PCA = 'agg_pca'
    # RUN_DATE = '2025_05_08_for_paper'
    # OUTPUT_FOLDER = os.path.join('figures', RUN_DATE, 'analysis_pca_reduced_ssd')

    # # only recommendations for the model prompt
    # local_df = df[df[C_STUDY_GROUP] == 'model' ]
    # run_analysis_pca_reduced_ssd_coordinates(local_df, OUTPUT_FOLDER, WHICH_PCA, f'aggregate__model_preference')

    # To run other analysis, you can filter df as is done above for the temperature and model name.
    # local_df = df[df['model'].isin([CLAUDE_3_5_HAIKU])]
    # local_df = local_df[local_df['prompt_type'] == LLM_AS_STUDENT]
    # local_df = local_df[local_df['temperature'] == 0.3]
    # run_analysis_pca_reduced_ssd_coordinates(local_df, OUTPUT_FOLDER, WHICH_PCA, f'TEMPORARY')
