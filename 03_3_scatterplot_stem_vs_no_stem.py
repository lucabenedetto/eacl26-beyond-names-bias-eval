from typing import List, Union, Tuple, Dict
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


def to_be_skipped_due_to_empty_recommendation(row):
    return (row.ssd_rec_0 == "NONE" or row.ssd_rec_1 == "NONE" or row.ssd_rec_2 == "NONE"
            or row.ssd_rec_3 == "NONE" or row.ssd_rec_4 == "NONE")


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
        if scores[index] is None:
            print(f"[INFO] Skipping item at index {index}, due to empty recommendation.")
        else:
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
        if to_be_skipped_due_to_empty_recommendation(row):
            x = None
        else:
            x = bool(row.is_stem_rec_0)*5 + bool(row.is_stem_rec_1)*4 + bool(row.is_stem_rec_2)*3 + bool(row.is_stem_rec_3)*2 + bool(row.is_stem_rec_4)*1
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
        if to_be_skipped_due_to_empty_recommendation(row):
            coordinate = None
        else:
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


def plot_distribution_stem_magnitude(stem_magnitudes: Dict[str, List[float]],
                                     title_model: str,
                                     title_promp_type: str,
                                     title_prompt_params: str,
                                     title_temp: str,
                                     ) -> None:
    """
    This method plots the distribution of the STEM magnitude passed as argument.
    :param stem_magnitudes:
    :param title_model:
    :param title_promp_type:
    :param title_prompt_params:
    :param title_temp:
    :return:
    """
    data = [stem_magnitudes[key] for key in stem_magnitudes.keys()]

    plt.figure()
    plt.boxplot(data, tick_labels=list(stem_magnitudes.keys()), patch_artist=True)
    plt.title(f'Distribution of STEM Magnitude: {title_model}|{title_promp_type}|{title_prompt_params}|{title_temp}')
    plt.xlabel('Study Group')
    plt.ylabel('STEM Magnitude')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Show the plot
    plt.show()


def tsne_clustering(coordinates: Dict[str, List[ndarray]],
                    title_model: str,
                    title_promp_type: str,
                    title_prompt_params: str,
                    title_temp: str,
                    ) -> None:
    """
    This method performs TSNE dimensionality reduction of the coordinates passed as argument.
    :param coordinates:
    :param title_model:
    :param title_promp_type:
    :param title_prompt_params:
    :param title_temp:
    :return:
    """
    # TODO test with other params, and make them tunable by changing the functions parameters.
    model = TSNE(n_components=2, perplexity=50, learning_rate=200, random_state=42)

    full_coordinates_list = coordinates['model'] + coordinates['f'] + coordinates['m'] + coordinates['x']
    transformed_full_list = model.fit_transform(np.array(full_coordinates_list))

    x_model = transformed_full_list[:len(coordinates['model'])]
    x_f = transformed_full_list[len(x_model):len(x_model)+len(coordinates['f'])]
    x_m = transformed_full_list[len(x_model)+len(x_f):len(x_model)+len(x_f)+len(coordinates['m'])]
    x_x = transformed_full_list[len(x_model)+len(x_f)+len(x_m):]

    fig, ax = plt.subplots()
    ax.scatter([x[0] for x in x_f], [x[1] for x in x_f], label='f', alpha=0.2)
    ax.scatter([x[0] for x in x_m], [x[1] for x in x_m], label='m', alpha=0.2)
    ax.scatter([x[0] for x in x_x], [x[1] for x in x_x], label='x', alpha=0.2)
    ax.scatter([x[0] for x in x_model], [x[1] for x in x_model], label='model', alpha=0.2)
    ax.legend()
    plt.title(f't-SNE: {title_model} | {title_promp_type} | {title_prompt_params} | {title_temp}')
    plt.show()


def main():
    # Change these params to run the evaluation and the plots on different models / prompts and update the titles, axes,
    #   etc. of the output images.
    lang = IT
    prompt_params = CONFIG_NO_NAME
    list_models = [GPT_3_5] # , GPT_3_5, GPT_4o, GPT_4o_MINI, CLAUDE_3_5_HAIKU, CLAUDE_3_5_SONNET, GEMINI_1_5_FLASH, GEMINI_1_5_FLASH_8B]:
    list_prompt_types = [USER_AS_STUDENT, LLM_AS_STUDENT]
    list_temperatures = [0.0, 0.3, 0.6]
    title_model = 'GPT_3_5'
    title_promp_type = 'UaS and LaS'
    title_prompt_params = 'No name'
    title_temp = 'all temps.'

    stem_magnitude = defaultdict(list)
    ssd_coordinates = defaultdict(list)
    for model in list_models:
        for prompt_type in list_prompt_types:
            for temp in list_temperatures:
                # Get the recommendations for the given model and prompt (the prompt is identified by prompt_type,
                #   prompt_params_file, and temperature)
                folder_path = os.path.join('data', 'processed_output', f'{prompt_type}', f'{lang}')
                df = pd.read_csv(os.path.join(folder_path, f'responses_{model}_{lang}_{prompt_params}_temp_{temp}.csv'))

                # Measure "how STEM" each recommendation is for the given model and prompt.
                new_stem_magnitude_values = compute_list_stem_magnitude_values(df)
                # Groups the values from new_stem_magnitude_values depending on their type (MODEL, F, M, X).
                grouped_stem_magnitude_values = group_scores_by_target_key(df, new_stem_magnitude_values)
                # Add the grouped values to the dict that collects the values for all the models in the loop.
                for key in grouped_stem_magnitude_values.keys():
                    stem_magnitude[key] += grouped_stem_magnitude_values[key]

                # Get the S.S.D ("settore scientifico disciplinare") coordinates for each recommendation.
                new_coordinates = compute_ssd_coordinates(df)
                grouped_ssd_coordinates = group_scores_by_target_key(df, new_coordinates)
                for key in grouped_ssd_coordinates.keys():
                    ssd_coordinates[key] += grouped_ssd_coordinates[key]

    plot_distribution_stem_magnitude(stem_magnitude, title_model, title_promp_type, title_prompt_params, title_temp)
    tsne_clustering(ssd_coordinates, title_model, title_promp_type, title_prompt_params, title_temp)


if __name__ == '__main__':
    main()
