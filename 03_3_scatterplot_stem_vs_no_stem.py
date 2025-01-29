from typing import List, Union, Tuple
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from numpy import ndarray
import os
import pandas as pd
from sklearn.manifold import TSNE
from constants import (
    IT, FR, EN,
    GPT_3_5, GPT_4o_MINI, GPT_4o,
    CLAUDE_3_5_SONNET, CLAUDE_3_5_HAIKU,
    GEMINI_1_5_FLASH_8B, GEMINI_1_5_FLASH,
    USER_AS_STUDENT, LLM_AS_STUDENT,
    FRIEND_AS_STUDENT,
    CONFIG_NO_NAME,
    CONFIG_W_NAMES,
    CONFIG_NO_NAME_W_PRONOUNS,
    NAMES_F, NAMES_M,
    ADJECTIVES_M, ADJECTIVES_F, ADJECTIVES_X,
    NOUNS_M, NOUNS_F, NOUNS_X,
)

# TODO move this to a different file
def get_target_dict_from_df_row(row) -> str:
    # Note that this does not distinguish between different adjectives (for any gender nor no gender, it groups them together).
    if not (row['with_name'] or row['with_noun'] or row['with_adjective']):
        return 'model'
    if row['with_name']:  # TODO: This does not work for parsing the rows with names if the adjective/noun is X instead of F/M
        if row['name'] in NAMES_F[row['language']]:
            return 'f'
        if row['name'] in NAMES_M[row['language']]:
            return 'm'
    if row['with_noun']:
        if row['noun'] in NOUNS_F[row['language']]:
            return 'f'
        if row['noun'] in NOUNS_M[row['language']]:
            return 'm'
        if row['noun'] in NOUNS_X[row['language']]:
            return 'x'
    if row['with_adjective']:
        if row['adjective'] in ADJECTIVES_F[row['language']]:
            return 'f'
        if row['adjective'] in ADJECTIVES_M[row['language']]:
            return 'm'
        if row['adjective'] in ADJECTIVES_X[row['language']]:
            return 'x'
    raise ValueError(f"Error with row ({row}).")


def group_scores_by_target_key(recommendations_df: pd.DataFrame, scores: List[Union[float, ndarray]]) -> defaultdict:
    """
    This method receives the dataframe with the list of recommendations and a list of scores (computed for instance with
    the method compute_list_stem_magnitude_values) and returns a defaultdict object, where the keys are the groups we
    are studying in the paper (MODEL, F, M, X) and the values are their scores.
    :param recommendations_df: a list of recommendations.
    :param scores: the scores computed for each recommendation.
    :return: a defaultdict object, where the keys are the groups we are studying in the paper (MODEL, F, M, X) and the
      values are their scores.
    """
    result = defaultdict(list)
    for index, (_, row) in enumerate(recommendations_df.iterrows()):
        target = get_target_dict_from_df_row(row)
        result[target].append(scores[index])
    return result


def compute_list_stem_magnitude_values(response_df: pd. DataFrame) -> List[float]:
    """
    This method computes the "stem magnitude" of the recommendations stored in the dataframe passed as argument.
    The "stem magnitude" is defined as follows:
    each element in the list of five recommendations is either STEM or not -- this info must be already available in the
    .csv file which contains the parsed responses (and it is if created with the script 02_parse_responses.py) -- and
    the "stem magnitude" is the sum of the weights of the STEM recommendations, where the weight is 5 for the first
    recommendation, 4 for the second recommendation, etc.
    This method performs the computation of the stem magnitude and returns a list where each element indicates the stem
    magnitude of the corresponding recommendation in the dataframe.
    :param response_df:
    :return:
    """
    list_stem_magnitude_values = []
    for index, row in response_df.iterrows():
        # TODO add check that I actually have to consider this recommendation (i.e. there is no NONE in it).
        x = row.is_stem_rec_0*5 + row.is_stem_rec_1*4 + row.is_stem_rec_2*3 + row.is_stem_rec_3*2 + row.is_stem_rec_4*1
        list_stem_magnitude_values.append(x)
    return list_stem_magnitude_values


def compute_ssd_coordinates(response_df: pd. DataFrame) -> List[ndarray]:
    """
    This method computes the SSD coordinates of the recommendations stored in the dataframe passed as argument.
    Each list of recommendations is converted into an array of 14 elements (because there are 14 S.S.D. in IT), where
    each value indicates the "magnitude" of that S.S.D. in the recommendation, similarly to what is done when computing
    the STEM magnitude.
    :param response_df: the dataframe containing the recommendations.
    :return: the list of SSD coordinates.
    """
    list_ssd_coordinates = []
    for _, row in response_df.iterrows():
        # TODO check that I actually have to consider this recommendation (i.e. there is no NONE in it).
        if (row.ssd_rec_0 == "NONE" or row.ssd_rec_1 == "NONE" or row.ssd_rec_2 == "NONE"
            or row.ssd_rec_3 == "NONE" or row.ssd_rec_4 == "NONE"):
            print("[INFO] skipping one row as it contains NONE.")
            continue
        # 'ssd_rec_*' can then be one of "01", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14" (for IT)
        coordinate = np.zeros(14)
        # TODO possibly make the below with a loop
        coordinate[int(row.ssd_rec_0)-1] += 5  # I need the "-1" because the ssd are between 01 and 14.
        coordinate[int(row.ssd_rec_1)-1] += 4
        coordinate[int(row.ssd_rec_2)-1] += 3
        coordinate[int(row.ssd_rec_3)-1] += 2
        coordinate[int(row.ssd_rec_4)-1] += 1
        list_ssd_coordinates.append(coordinate)
    return list_ssd_coordinates


def plot_distribution_stem_magnitude(coordinates):
    fig, ax = plt.subplots(1, len(coordinates.keys()), sharex=True, sharey=True)
    for idx, key in enumerate(coordinates.keys()):
        ax[idx].hist(coordinates[key], bins=5, label=key)
        ax[idx].legend()
        ax[idx].grid(axis='y')
    plt.show()


def clustering_ssd(coordinates):
    # TODO dimensionality reduction with either PCA or t-SNE, then scatter plot.
    model = TSNE(n_components=2, perplexity=50, learning_rate=200, random_state=42)  # TODO test with other params
    full_list = coordinates['model'] + coordinates['f'] + coordinates['m'] + coordinates['x']
    transformed_full_list = model.fit_transform(np.array(full_list))
    x_model = transformed_full_list[:len(coordinates['model'])]
    x_f = transformed_full_list[len(x_model):len(x_model)+len(coordinates['f'])]
    x_m = transformed_full_list[len(x_model)+len(x_f):len(x_model)+len(x_f)+len(coordinates['m'])]
    x_x = transformed_full_list[len(x_model)+len(x_f)+len(x_m):]
    fig, ax = plt.subplots()
    ax.scatter([x[0] for x in x_f], [x[1] for x in x_f], label='f', alpha=0.3)
    ax.scatter([x[0] for x in x_m], [x[1] for x in x_m], label='m', alpha=0.3)
    ax.scatter([x[0] for x in x_x], [x[1] for x in x_x], label='x', alpha=0.3)
    ax.scatter([x[0] for x in x_model], [x[1] for x in x_model], label='model', alpha=0.3)
    ax.legend()
    plt.show()


def main():
    LANGUAGE = IT
    PROMPT_PARAMS_FILE = CONFIG_NO_NAME
    stem_magnitude = defaultdict(list)
    coordinates = defaultdict(list)
    for MODEL in [GPT_3_5]: # , GPT_4o, GPT_4o_MINI, CLAUDE_3_5_HAIKU, CLAUDE_3_5_SONNET, GEMINI_1_5_FLASH, GEMINI_1_5_FLASH_8B]:
        for PROMPT_TYPE in [USER_AS_STUDENT, LLM_AS_STUDENT]:
            for TEMP in [0.0, 0.3, 0.6]:
                # Get the recommendations for the given model and prompt (the prompt is identified by prompt_type,
                #   prompt_params_file, and temperature)
                folder_path = os.path.join('data', 'processed_output', f'{PROMPT_TYPE}', f'{LANGUAGE}')
                df = pd.read_csv(os.path.join(folder_path, f'responses_{MODEL}_{LANGUAGE}_{PROMPT_PARAMS_FILE}_temp_{TEMP}.csv'))

                # Measure "how STEM" each recommendation is for the given model and prompt.
                new_stem_magnitude_values = compute_list_stem_magnitude_values(df)
                # Groups the values from new_stem_magnitude_values depending on their type (MODEL, F, M, X).
                grouped_stem_magnitude_values = group_scores_by_target_key(df, new_stem_magnitude_values)
                # Add the grouped values to the dict that collects the values for all the models in the loop.
                for key in grouped_stem_magnitude_values.keys():
                    stem_magnitude[key] += grouped_stem_magnitude_values[key]

                # Get the S.S.D ("settore scientifico disciplinare") coordinates for each recommendation.
                # new_coordinates = compute_ssd_coordinates(MODEL, LANGUAGE, PROMPT_TYPE, PROMPT_PARAMS_FILE, TEMP)
                new_coordinates = compute_ssd_coordinates(df)
                grouped_ssd_coordinates = group_scores_by_target_key(df, new_coordinates)
                for key in grouped_ssd_coordinates.keys():
                    coordinates[key] += grouped_ssd_coordinates[key]

                # coordinates['model'] += new_coordinates['model']
                # coordinates['f'] += new_coordinates['f']
                # coordinates['m'] += new_coordinates['m']
                # coordinates['x'] += new_coordinates['x']

    # TODO below
    plot_distribution_stem_magnitude(stem_magnitude)
    clustering_ssd(coordinates)


if __name__ == '__main__':
    main()
