import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from constants import (
    MODELS_LIST,
    STUDY_GROUPS,
    COLOUR_BY_GROUP,
)
from course_mappings import LIST_SSD_EN


plt.rcParams.update({
    "font.size": 16,
    "font.family": "serif",
})


def plot_barh_recommendations_per_study_group(df, study_groups, colors, run_date, output_name = None):
    ssd_rank_per_study_group = {}
    for study_group in study_groups:
        local_df = df[df['study_group'] == study_group]
        ssd_rank_per_study_group[study_group] = [local_df[f'SSD_{idx}'].mean() for idx in range(14)]

    for study_group in study_groups:
        # Do not plot if missing data.
        if np.isnan(ssd_rank_per_study_group[study_group][0]):
            return


    fig, ax = plt.subplots(figsize=(14, 6))

    n_sources = len(ssd_rank_per_study_group.keys())
    n_ssds = len(LIST_SSD_EN)

    y_pos = np.arange(n_ssds)
    bar_height = 0.15
    total_height = n_sources * bar_height
    y_offsets = y_pos - (total_height - bar_height) / 2

    for i, (study_group, ssd_rank) in enumerate(ssd_rank_per_study_group.items()):
        ax.barh(y_offsets + i * bar_height, ssd_rank, height=bar_height, label=study_group, color=colors[study_group])

    ax.set_yticks(y_pos)
    ax.set_yticklabels(LIST_SSD_EN)
    ax.set_ylabel('SSD Name')

    ax.set_xticks(range(6))
    ax.grid()
    ax.set_xlabel('Recommendation score')
    ax.legend()

    plt.tight_layout()
    if output_name is not None:
        plt.savefig(os.path.join('figures', run_date, output_name))
        plt.close()
    else:
        plt.show()

def main(run_date):
    df = pd.read_csv(os.path.join('data', 'processed_output', 'stem_magnitude_ssd_coordinates_recs.csv'))
    for model in MODELS_LIST:
        # For the individual models
        plot_barh_recommendations_per_study_group(
            df[df['model'] == model], STUDY_GROUPS, COLOUR_BY_GROUP, run_date=run_date, output_name=f'appendix_recs_per_study_group_{model}.pdf'
        )


if __name__ == '__main__':
    RUN_DATE = "2025_09_29_for_paper"
    main(RUN_DATE)
