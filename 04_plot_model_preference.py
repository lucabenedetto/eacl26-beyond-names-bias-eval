import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from constants import (
    COLOUR_BY_GROUP,
    OPENAI_MODEL_TO_API_NAME,
    GOOGLE_MODEL_TO_API_NAME,
    ANTHROPIC_MODEL_TO_API_NAME,
)
from course_mappings import LIST_SSD_EN


plt.rcParams.update({
    "font.size": 16,
    "font.family": "serif",
})


def plot_barh_baseline_preferences_per_model(df, model_names, colors, run_date, output_name = None):
    ssd_rank_per_model = {}
    df = df[df['study_group'] == 'model']
    for model_name in model_names:
        local_df = df[df['model'] == model_name]
        ssd_rank_per_model[model_name] = [local_df[f'SSD_{idx}'].mean() for idx in range(14)]

    fig, ax = plt.subplots(figsize=(14, 6))

    n_sources = len(ssd_rank_per_model.keys())
    n_ssds = len(LIST_SSD_EN)

    y_pos = np.arange(n_ssds)
    bar_height = 0.15
    total_height = n_sources * bar_height
    y_offsets = y_pos - (total_height - bar_height) / 2

    for i, (model_name, ssd_rank) in enumerate(ssd_rank_per_model.items()):
        ax.barh(y_offsets + i * bar_height, ssd_rank, height=bar_height, label=model_name, color=colors[i])

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
    df = df[df['study_group'] == 'model']
    ssd_rank = [df[f'SSD_{idx}'].mean() for idx in range(14)]

    # Aggregate across models
    fig, ax = plt.subplots(figsize=(14, 4))
    ax.barh(range(14), ssd_rank, color=COLOUR_BY_GROUP['model'])

    ax.set_yticks(range(14))
    ax.set_yticklabels(LIST_SSD_EN)

    ax.set_ylabel('SSD Name')
    ax.set_xlabel('Recommendation score')

    plt.tight_layout()
    # plt.show()
    plt.savefig(os.path.join('figures', run_date, 'model_preferences_aggregate.pdf'))
    plt.close()

    # For the individual models
    plot_barh_baseline_preferences_per_model(
        df, list(OPENAI_MODEL_TO_API_NAME.keys()), colors=["#90EE90", "#3CB371", "#2E8B57", "#228B22", "#006400"],
        run_date=run_date, output_name='model_preferences_openai.pdf'
    )
    plot_barh_baseline_preferences_per_model(
        df, list(ANTHROPIC_MODEL_TO_API_NAME.keys()), ["#FFD580", "#FFA500", "#CC5500"],
        run_date=run_date, output_name = 'model_preferences_anthropic.pdf'
    )
    plot_barh_baseline_preferences_per_model(
        df, list(GOOGLE_MODEL_TO_API_NAME.keys()), ["#87CEFA", "#4682B4", "#00008B"],
        run_date=run_date, output_name='model_preferences_google.pdf'
    )


if __name__ == '__main__':
    RUN_DATE = "2025_09_29_for_paper"
    main(RUN_DATE)
