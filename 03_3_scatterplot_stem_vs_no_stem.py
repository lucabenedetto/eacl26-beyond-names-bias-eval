from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
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


def compute_stem_magnitude(model, language, prompt_type, prompt_params_file, temperature):
    folder_path = os.path.join('data', 'processed_output', f'{prompt_type}', f'{language}')
    df = pd.read_csv(os.path.join(folder_path, f'responses_{model}_{language}_{prompt_params_file}_temp_{temperature}.csv'))
    result = defaultdict(list)
    for index, row in df.iterrows():
        # TODO check that I actually have to consider this recommendation (i.e. there is no NONE in it).
        x = row.is_stem_rec_0*5 + row.is_stem_rec_1*4 + row.is_stem_rec_2*3 + row.is_stem_rec_3*2 + row.is_stem_rec_4*1
        # Add the coordinates to the relevant key.
        target = get_target_dict_from_df_row(row)
        result[target].append(x)
        # result['m'].append(x)
        # result['x'].append(x)
    return result


def compute_ssd_coordinates(model, language, prompt_type, prompt_params_file, temperature):
    # TODO: almost the same as the method above, but considers the ~14 s.s.d. instead of the binary stem-not stem
    #   categorisation. Then I have to do PCA or t-SNE to show the clustering.
    folder_path = os.path.join('data', 'processed_output', f'{prompt_type}', f'{language}')
    df = pd.read_csv(os.path.join(folder_path, f'responses_{model}_{language}_{prompt_params_file}_temp_{temperature}.csv'))
    result = defaultdict(list)
    for _, row in df.iterrows():
    # for row in df.itertuples():
        # TODO check that I actually have to consider this recommendation (i.e. there is no NONE in it).
        if (row.ssd_rec_0 == "NONE" or row.ssd_rec_1 == "NONE" or row.ssd_rec_2 == "NONE"
            or row.ssd_rec_3 == "NONE" or row.ssd_rec_4 == "NONE"):
            print("[INFO] skipping one row as it contains NONE.")
            continue
        # 'ssd_rec_o'  can then be one of "01", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14"
        # one recommended list is converted into an array of 14 elements (2 will always be 0).
        coordinate = np.zeros(14)  # This works only for language = IT.
        # TODO make the below with a loop
        coordinate[int(row.ssd_rec_0)-1] += 5  # I need the "-1" because the ssd are between 01 and 14.
        coordinate[int(row.ssd_rec_1)-1] += 4  # I need the "-1" because the ssd are between 01 and 14.
        coordinate[int(row.ssd_rec_2)-1] += 3  # I need the "-1" because the ssd are between 01 and 14.
        coordinate[int(row.ssd_rec_3)-1] += 2  # I need the "-1" because the ssd are between 01 and 14.
        coordinate[int(row.ssd_rec_4)-1] += 1  # I need the "-1" because the ssd are between 01 and 14.

        # Add the coordinates to the relevant key.
        target = get_target_dict_from_df_row(row)
        result[target].append(coordinate)
    return result

    pass


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


LANGUAGE = IT
PROMPT_PARAMS_FILE = CONFIG_NO_NAME
if __name__ == '__main__':
    stem_magnitude = defaultdict(list)
    coordinates = defaultdict(list)
    for MODEL in [GPT_3_5]: # , GPT_4o, GPT_4o_MINI, CLAUDE_3_5_HAIKU, CLAUDE_3_5_SONNET, GEMINI_1_5_FLASH, GEMINI_1_5_FLASH_8B]:
        for PROMPT_TYPE in [USER_AS_STUDENT, LLM_AS_STUDENT]:
            for TEMP in [0.0, 0.3, 0.6]:
                # print(f"[INFO] Doing Model {MODEL} | Language {IT} | Temperature {TEMPERATURE} | Prompt type {PROMPT_TYPE} | Prompt params file {PROMPT_PARAMS_FILE}.")
                new_stem_magnitude = compute_stem_magnitude(MODEL, LANGUAGE, PROMPT_TYPE, PROMPT_PARAMS_FILE, TEMP)
                stem_magnitude['model'] += new_stem_magnitude['model']
                stem_magnitude['f'] += new_stem_magnitude['f']
                stem_magnitude['m'] += new_stem_magnitude['m']
                stem_magnitude['x'] += new_stem_magnitude['x']

                new_coordinates = compute_ssd_coordinates(MODEL, LANGUAGE, PROMPT_TYPE, PROMPT_PARAMS_FILE, TEMP)
                coordinates['model'] += new_coordinates['model']
                coordinates['f'] += new_coordinates['f']
                coordinates['m'] += new_coordinates['m']
                coordinates['x'] += new_coordinates['x']

    # TODO below
    plot_distribution_stem_magnitude(stem_magnitude)
    clustering_ssd(coordinates)