import os
from collections import defaultdict

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from constants import (
    IT, FR, EN,
    GPT_3_5, GPT_4o_MINI,
    CLAUDE_3_5_SONNET, CLAUDE_3_5_HAIKU,
    GEMINI_1_5_FLASH_8B, GEMINI_1_5_FLASH,
    USER_AS_STUDENT, LLM_AS_STUDENT,
    NAMES_F, NAMES_M,
    ADJECTIVES_M, ADJECTIVES_F, ADJECTIVES_X,
    NOUNS_M, NOUNS_F, NOUNS_X,
)
from utils import get_target_dict_from_df_row


def main(language, model, prompt_params_file, prompt_type):
    # Load the DF
    df = pd.read_csv(f'data/interim/count_recommended_courses_aggregate_{model}_{language}.csv')
    # Filter courses to keep only the 10 most frequent
    print(f"Count value of the 11th course = {df['count'].values[10]} ({df['course'].values[10]})")
    df = df[:10].copy()

    # Prepare dicts which will have the positions of the different courses.
    course_ranking = {
        'model': defaultdict(list),
        'f': defaultdict(list),
        'm': defaultdict(list),
        'x': defaultdict(list),
    }

    # Iterate over all the exp. results that I want to consider, separately for the different study groups (M/F/X)
    for temperature in [0.0, 0.3, 0.6]:
        folder_path = os.path.join('data', 'processed_output', f'{prompt_type}', f'{language}')
        local_df = pd.read_csv(os.path.join(folder_path, f'responses_{model}_{language}_{prompt_params_file}_temp_{temperature}.csv'))
        # For each one, loop over the rows
        for _, row in local_df.iterrows():
            # TODO: it is here, that I have to specify the different study groups (e.g. uno/una/un*)
            target_dict = get_target_dict_from_df_row(row)

            # For each course
            for course in df['course'].values:
                # Append score from its position (the higher, the better), or 0 if it is not in the list of recommended courses
                found_match = False
                for idx in range(5):  # TODO make this 5 a param
                    if row[f'rec_{idx}'] == course:
                        found_match = True
                        course_ranking[target_dict][course].append(5 - idx)  # TODO make this 5 a param
                if not found_match:
                    course_ranking[target_dict][course].append(0)

    plot_comparative_bar_plot(course_ranking, model, prompt_params_file, prompt_type)
    # The code below creates one bar plot for each study group
    # for mode in course_ranking.keys():
    #     fig, ax = plt.subplots()
    #     xs = list(course_ranking[mode].keys())
    #     ys = [np.mean(course_ranking[mode][x]) for x in xs]
    #     std = [np.std(course_ranking[mode][x]) for x in xs]
    #     ax.bar(xs, ys, yerr=std)
    #     ax.set_xticks(xs)
    #     truncated_labels = [label[:15] + '...' if len(label) > 15 else label[:15] for label in xs]
    #     ax.set_xticklabels(truncated_labels, rotation=90)
    #     ax.grid(axis='y')
    #     ax.set_title(mode)
    #     ax.set_ylim(0, 5)
    #     plt.tight_layout()
    #     plt.savefig(f'figures/first_test_{model}__{prompt_params_file}__{prompt_type}_{mode}.png')


def plot_comparative_bar_plot(course_ranking, model, prompt_params_file, prompt_type):
    courses = course_ranking['x'].keys()  # Using 'x' because model is not in the dict for the 'with_name' exps.
    data_means = {
        'model': [np.mean(course_ranking['model'][x]) for x in courses],
        'm': [np.mean(course_ranking['m'][x]) for x in courses],
        'f': [np.mean(course_ranking['f'][x]) for x in courses],
        'x': [np.mean(course_ranking['x'][x]) for x in courses],
    }
    data_stds = {
        'model': [np.std(course_ranking['model'][x]) for x in courses],
        'm': [np.std(course_ranking['m'][x]) for x in courses],
        'f': [np.std(course_ranking['f'][x]) for x in courses],
        'x': [np.std(course_ranking['x'][x]) for x in courses],
    }

    columns = list(data_means.keys())
    values = np.array(list(data_means.values()))
    std_values = np.array(list(data_stds.values()))

    n_study_groups = len(columns)

    x = np.arange(len(courses))

    bar_width = 0.2

    fig, ax = plt.subplots(figsize=(14, 10))
    for i in range(n_study_groups):
        ax.bar(x + i * bar_width, values[i], yerr=std_values[i], width=bar_width, label=columns[i])
    ax.grid(axis='y')
    ax.set_xticks(x + bar_width * (n_study_groups - 1) / 2)
    # ax.set_xticklabels(courses, rotation=90)
    truncated_labels = [label[:15] + '...' if len(label) > 15 else label[:15] for label in courses]
    ax.set_xticklabels(truncated_labels, rotation=90)
    ax.set_ylim(-1, 6)
    ax.set_xlabel('Courses')
    ax.set_ylabel('Values')
    ax.set_title(f'Ranking recommended degrees | {model} | {prompt_params_file} | {prompt_type}')
    ax.legend()

    # Show plot
    plt.tight_layout()
    plt.show()
    # plt.savefig(f'figures/first_test__{prompt_params_file}__{prompt_type}__{model}.png')


if __name__ == '__main__':
    LANGUAGE = IT
    PROMPT_PARAMS_FILE = 'no_name'  # 'with_names', 'no_name'
    for PROMPT_TYPE in [USER_AS_STUDENT, LLM_AS_STUDENT]:  #  USER_AS_STUDENT
        for MODEL in [GPT_3_5, GPT_4o_MINI, GEMINI_1_5_FLASH_8B, GEMINI_1_5_FLASH, CLAUDE_3_5_HAIKU]:
            main(LANGUAGE, MODEL, PROMPT_PARAMS_FILE, PROMPT_TYPE)
