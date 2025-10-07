import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from constants import COLOUR_BY_GROUP
from course_mappings import LIST_SSD_EN


plt.rcParams.update({
    "font.size": 16,
    "font.family": "serif",
})


def plot_barh_baseline_preferences_per_model(df, run_date, output_name=None):

    n_ssds = 7  # 10 so that I only show the first 10 (which are the most frequently recommended).
    start_idx = 14-n_ssds

    ssd_rank_per_study_group = {}
    for study_group in ['m', 'x', 'f']:
        local_df = df[df['study_group'] == study_group]
        ssd_rank_per_study_group[study_group] = [local_df[f'SSD_{idx}'].mean() for idx in range(start_idx,14)]

    fig, ax = plt.subplots(figsize=(14, 4))

    n_sources = len(ssd_rank_per_study_group.keys())

    y_pos = np.arange(n_ssds)
    bar_height = 0.2
    total_height = n_sources * bar_height
    y_offsets = y_pos - (total_height - bar_height) / 2

    for i, (model_name, ssd_rank) in enumerate(ssd_rank_per_study_group.items()):
        ax.barh(y_offsets + i * bar_height, ssd_rank, height=bar_height, label=model_name.upper(), color=COLOUR_BY_GROUP[model_name])

    ax.set_yticks(y_pos)
    ax.set_yticklabels(LIST_SSD_EN[start_idx:])
    ax.set_ylabel('Disciplinary sector')

    ax.set_xticks(range(6))
    ax.grid(axis='x')
    ax.set_xlabel('Recommendation score')
    ax.legend()

    plt.tight_layout()
    if output_name is not None:
        plt.savefig(os.path.join('figures', run_date, output_name))
        plt.close()
    else:
        plt.show()

if __name__ == '__main__':
    RUN_DATE = "2025_09_29_for_paper"
    df = pd.read_csv(os.path.join('data', 'processed_output', 'stem_magnitude_ssd_coordinates_recs.csv'))
    # plot_barh_baseline_preferences_per_model(df, run_date=RUN_DATE, output_name=None)
    plot_barh_baseline_preferences_per_model(df, run_date=RUN_DATE, output_name='intro_figure.pdf')
