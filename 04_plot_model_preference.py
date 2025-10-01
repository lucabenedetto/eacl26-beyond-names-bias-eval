import os
import pandas as pd
import matplotlib.pyplot as plt
from constants import COLOUR_BY_GROUP
from course_mappings import LIST_SSD_EN

plt.rcParams.update({
    "font.size": 16,
    "font.family": "serif",
})

def main(run_date):
    df = pd.read_csv(os.path.join('data', 'processed_output', 'stem_magnitude_ssd_coordinates_recs.csv'))
    df = df[df['study_group'] == 'model']
    ssd_rank = [df[f'SSD_{idx}'].mean() for idx in range(14)]

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



if __name__ == '__main__':
    RUN_DATE = "2025_09_29_for_paper"
    main(RUN_DATE)
