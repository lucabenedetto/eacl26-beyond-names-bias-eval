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
    MODELS_BY_OWNER,
    MODELS_LIST,
    USER_AS_STUDENT, 
    LLM_AS_STUDENT,
    CONFIG_W_NAMES,
    CONFIG_NO_NAME,
    CLAUDE_3_5_HAIKU,
)

plt.rcParams.update({
    "font.size": 16,
    "font.family": "serif",
})


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
        plt.close()
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
        plt.close()
    else:
        plt.show()


# method for computing the EMD between the distribution of STEM magnitudes of the recommendations for different groups and plotting a conf mat.
def confusion_matrix_stem_magnitude_distance(
        df,
        class_column,
        x_column,
        vmax=3,
        output_file=None,
):
    # TODO: possibly change this so that it doesn't use the EMD by default but rather I can pass the method.
    n_study_groups = df[class_column].nunique()
    if len(STUDY_GROUPS) != n_study_groups:
        print(f"[WARNING]T he number of study groups in the DF ({n_study_groups}) is not the expected one {len(STUDY_GROUPS)}.")

    conf_mat = np.zeros((n_study_groups, n_study_groups))

    # I am using this order instead of the original one in the constant STUDY_GROUPS because it better highlights the trends in the heatmaps.
    reordered_study_groups = ['model', 'm', 'x', 'f']
    reordered_study_groups = [x for x in reordered_study_groups if x in df[class_column].unique()]
    for (idx_1, study_group_1) in enumerate(reordered_study_groups):
        stem_magnitudes_1 = df[df[class_column] == study_group_1][x_column].tolist()
        for (idx_2, study_group_2) in enumerate(reordered_study_groups):
            stem_magnitudes_2 = df[df[class_column] == study_group_2][x_column].tolist()
            conf_mat[idx_1, idx_2] = wasserstein_distance(stem_magnitudes_1, stem_magnitudes_2)

    # print('Confusion matrix')
    # print(conf_mat)

    fig, ax = plt.subplots(figsize=(6, 6))
    im = ax.imshow(conf_mat, cmap='Reds', vmax=vmax)
    # Show all ticks and label them with the respective list entries
    ax.set_xticks(range(len(reordered_study_groups)), labels=[x.title() for x in reordered_study_groups])
    ax.set_yticks(range(len(reordered_study_groups)), labels=[x.title() for x in reordered_study_groups], rotation=90)
    # Loop over data dimensions and create text annotations.
    for i in range(len(reordered_study_groups)):
        for j in range(len(reordered_study_groups)):
            text = ax.text(j, i, "%.2f" % conf_mat[i, j], ha="center", va="center")
    # TODO finalise title.
    ax.set_title("EMD | STEM Magnitudes")
    fig.tight_layout()
    if output_file:
        plt.savefig(output_file)
        plt.close()
    else:
        plt.show()


def run_analysis_stem_magnitude(df, output_folder, which_model_and_params):
    print("Doing violinplot distribution of STEM magnitude by study group.")
    violinplot_stem_magnitude_by_study_group(
        df, C_STUDY_GROUP, C_STEM_MAGNITUDE,
        output_file=os.path.join(output_folder, f'{which_model_and_params}__violinplot_stem_magnitude_by_class.png'),
    )

    print("Doing histogram of the distribution of STEM magnitude by study group.")
    plot_histogram_by_class(
        df, C_STUDY_GROUP, C_STEM_MAGNITUDE, 
        output_file=os.path.join(output_folder, f'{which_model_and_params}__hist_stem_magnitude_by_class.png'),
    )

    print("Doing confusion matrix EMD of STEM magnitude")
    confusion_matrix_stem_magnitude_distance(
        df, C_STUDY_GROUP, C_STEM_MAGNITUDE,
        output_file=os.path.join(output_folder, f'{which_model_and_params}__conf_mat_EMD_stem_magnitude_by_class.png'),
        )


def run_complete_analyais_stem_magnitude(df, OUTPUT_FOLDER):
    # analysis on the aggregate dataframe
    run_analysis_stem_magnitude(df, OUTPUT_FOLDER, 'aggregate')

    for model_owner, list_models in MODELS_BY_OWNER.items():
        local_df = df[df['model'].isin(list_models)]
        run_analysis_stem_magnitude(local_df, OUTPUT_FOLDER, model_owner)

    # Analysis on different temperature values
    for temperature in [0.0, 0.3, 0.6]:
        local_df = df[df['temperature'] == temperature]
        run_analysis_stem_magnitude(local_df, OUTPUT_FOLDER, f'aggregate_temp_{temperature}')
    for temperatures in [[0.0, 0.3], [0.3, 0.6]]:
        local_df = df[df['temperature'].isin(temperatures)]
        run_analysis_stem_magnitude(local_df, OUTPUT_FOLDER, f'aggregate_temp_{temperatures[0]}_{temperatures[1]}')

    # analysis on different temperature values and different models
    for model_owner, list_models in MODELS_BY_OWNER.items():
        for temperature in [0.0, 0.3, 0.6]:
            local_df = df[df['model'].isin(list_models)]
            local_df = local_df[local_df['temperature'] == temperature]
            run_analysis_stem_magnitude(local_df, OUTPUT_FOLDER, f'{model_owner}_temp_{temperature}')

    # analysis on the individual models
    for model in MODELS_LIST:
        local_df = df[df['model'] == model]
        run_analysis_stem_magnitude(local_df, OUTPUT_FOLDER, model)

    # analysis on the different prompt types
    for prompt_type in [USER_AS_STUDENT, LLM_AS_STUDENT]:
        local_df = df[df['prompt_type'] == prompt_type]
        run_analysis_stem_magnitude(local_df, OUTPUT_FOLDER, f'aggregate_{prompt_type}')

    # analysis on the different prompt types and families of models
    for model_owner, list_models in MODELS_BY_OWNER.items():
        for prompt_type in [USER_AS_STUDENT, LLM_AS_STUDENT]:
            local_df = df[df['model'].isin(list_models)]
            local_df = local_df[local_df['prompt_type'] == prompt_type]
            run_analysis_stem_magnitude(local_df, OUTPUT_FOLDER, f'{model_owner}_{prompt_type}')


if __name__ == '__main__':
    df = pd.read_csv(os.path.join('data', 'processed_output', 'stem_magnitude_ssd_coordinates_recs.csv'))

    RUN_DATE = '2025_05_for_paper'
    # OUTPUT_FOLDER = os.path.join('figures', RUN_DATE, 'analysis_stem_magnitude')

    print("Doing both with and without names")
    OUTPUT_FOLDER = os.path.join('figures', RUN_DATE, 'analysis_stem_magnitude_aggregate')
    run_complete_analyais_stem_magnitude(df, OUTPUT_FOLDER)

    print("Doing without names")
    OUTPUT_FOLDER = os.path.join('figures', RUN_DATE, 'analysis_stem_magnitude_no_names')
    run_complete_analyais_stem_magnitude(df[df['prompt_param'] == CONFIG_NO_NAME], OUTPUT_FOLDER)

    print("Doing with names")
    OUTPUT_FOLDER = os.path.join('figures', RUN_DATE, 'analysis_stem_magnitude_with_names')
    run_complete_analyais_stem_magnitude(df[df['prompt_param'] == CONFIG_W_NAMES], OUTPUT_FOLDER)


    # # To run single analyses.
    # RUN_DATE = '2025_05_08_for_paper'
    # OUTPUT_FOLDER = os.path.join('figures', RUN_DATE, 'analysis_stem_magnitude')

    # # only recommendations for the model prompt
    # local_df = df[df[C_STUDY_GROUP] == 'model' ]
    # run_analysis_stem_magnitude(local_df, OUTPUT_FOLDER, f'aggregate__model_preference')
    # # local_df = df[df['model'].isin([CLAUDE_3_5_HAIKU])]
    # # local_df = local_df[local_df['prompt_type'] == LLM_AS_STUDENT]
    # # local_df = local_df[local_df['temperature'] == 0.3]
    # # run_analysis_stem_magnitude(local_df, OUTPUT_FOLDER, f'TEMPORARY')
