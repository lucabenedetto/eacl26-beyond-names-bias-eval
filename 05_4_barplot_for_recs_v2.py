import ast
import os
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from constants import (
    C_STUDY_GROUP,
    C_LIST_SSD,
    MAP_MODEL_TO_OWNER,
    COLOUR_BY_GROUP,
)
from course_mappings import LIST_SSD_EN


plt.rcParams.update({
    "font.size": 16,
    "font.family": "serif",
})


# TODO: Possibly move these to the constants or course mappings file.
MAP_SSD_ID_TO_NAME = {ssd: LIST_SSD_EN[idx] for idx, ssd in enumerate(C_LIST_SSD)}
print(MAP_SSD_ID_TO_NAME)
CUSTOM_ORDER = ['Model', 'M', 'X', 'F']


def compute_df_for_bar_plot_visualisation(df: pd.DataFrame, group_by_column: str):
    df_recommended_ssd_count = df.groupby(group_by_column).sum()[C_LIST_SSD]
    # this DF has one row for each study group, and one column for each SSD. The value of each cell is the frequency of the recommendation of the corresponding SSD (normalised)
    df_normalized = df_recommended_ssd_count.div(df_recommended_ssd_count.sum(axis=1), axis=0).reset_index()
    print(df_normalized)

    # pd.melt is turning wide-format data into long-format
    df_melted = pd.melt(df_normalized, id_vars=[group_by_column], var_name='SSD', value_name='Score')
    # print(df_melted)
    df_melted['ssd_name'] = df_melted.apply(lambda r: MAP_SSD_ID_TO_NAME[r['SSD']], axis=1)
    print(df_melted)

    return df_melted


def filter_to_keep_top_n_recommendations(df_melted: pd.DataFrame, top_n: int = 5):
        top_recs = df_melted.groupby("ssd_name")["Score"].mean().sort_values(ascending=False)[:top_n]
        return df_melted[df_melted['ssd_name'].isin(top_recs.index)], top_recs


def main():
    OUTPUT_FOLDER = './figures/2025_05_for_paper/bar_plot_recommendation_frequency/'
    data_path = "./data/processed_output/stem_magnitude_ssd_coordinates_recs.csv"  # changed this myself
    df = pd.read_csv(data_path)

    # These should be changed depending on the filter applied to the DF (see below).
    CURRENT_MODEL = 'aggregate'
    PROMPT_TYPE = 'aggregate'

    # Before this, you can add the filter on model / prompt type / etc.
    df_melted = compute_df_for_bar_plot_visualisation(df, C_STUDY_GROUP)
    df_melted['Study group'] = df_melted.apply(lambda r: r[C_STUDY_GROUP].title(), axis=1)

    fitlered_df_melted, top_recs = filter_to_keep_top_n_recommendations(df_melted, top_n=5)

    # Here is the code for the plot.
    fig = plt.figure(figsize=(16, 6))
    # fig.suptitle(f"Model: {CURRENT_MODEL}, Prompt Type: {PROMPT_TYPE}")
    ax = fig.add_subplot(1, 1, 1)
    sns.barplot(fitlered_df_melted, x="Score", y="ssd_name", hue='Study group', order=top_recs.index, orient="y", palette=COLOUR_BY_GROUP, hue_order=CUSTOM_ORDER)
    ax.grid(axis='x')
    ax.set_ylabel('SSD Name')
    ax.set_xlabel('Recommendation frequency')
    plt.tight_layout()
    # plt.show()
    plt.savefig(os.path.join(OUTPUT_FOLDER, 'image_for_introduction.png'))

    # This is the plot with only the stats about the model study group (TODO: should we have mean +/- std dev instead of the sum of the scores??).
    fig = plt.figure(figsize=(16, 9))
    fig.suptitle(f"Model preferences")
    ax = fig.add_subplot(1, 1, 1)
    sns.barplot(df_melted[df_melted['study_group'] == 'model'], x="Score", y="ssd_name", hue=C_STUDY_GROUP, orient="y")
    plt.tight_layout()
    plt.show()
    # TODO: save this as image.

    # Below the code for showing the preferences of individual models.
    model_df = compute_df_for_bar_plot_visualisation(df, 'model')
    model_df['model_owner'] = model_df.apply(lambda r: MAP_MODEL_TO_OWNER[r['model']], axis=1)
    print(model_df.drop('model', axis=1))
    # preferences for individual models
    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_subplot(1, 1, 1)
    sns.barplot(model_df, x="Score", y="ssd_name", hue='model', orient="y")
    plt.tight_layout()
    plt.show()
    # # preferences for model families
    # fig = plt.figure(figsize=(16, 9))
    # ax = fig.add_subplot(1, 1, 1)
    # sns.barplot(model_df, x="Score", y="ssd_name", hue='model_owner', orient="y")
    # plt.tight_layout()
    # plt.show()


if __name__ == '__main__':
    main()
