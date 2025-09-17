"""
This script takes the parsed recommendations, converts them into feature arrays using two different techniques, and
stores the converted feature arrays (into a single DataFrame for all the models).
It is meant to be run after the `02_parse_responses.py` script, and to be run once on all the models and prompt types.
In case of additional experiments, it can be re-run on the specific model/prompt, but then you have to concat the two
 dataframes (or you can re-run it on all the experiments since there is not that much data).
The two feature arrays are obtained as follows:
1. STEM magnitude: each recommended course is either STEM or not-STEM -- we use the official mapping available from the
   Italian ministry of education. The STEM magnitude is a number (in the range [0; 15] when 5 courses are recommended)
   indicating the number (and position) of STEM courses in the recommendations. The higher the STEM magnitude, the more
   STEM courses are recommended.
2. S.S.D. coordinates: S.S.D. means "settore scientifico disciplinare", and can be seen as the "areas" or "topics" of
   different university courses. The mapping between each recommendation and the corresponding S.S.D. is performed with
   the constant available in the `course_mappings.py` file (and is performed by the `02_parse_responses.py` script). The
   S.S.D. coordinates are obtained by converting the recommendations into a feature array where each element indicates
   the "magnitude" of that S.S.D. in the recommendations.
"""
from typing import List
import pandas as pd
import numpy as np
import os

from utils import (
    to_be_skipped_due_to_empty_recommendation,
    get_target_dict_from_df_row,
)
from constants import (
    IT,
    MODELS_LIST,
    USER_AS_STUDENT, LLM_AS_STUDENT, THIRD_PERSON_AS_STUDENT,
    CONFIG_NO_NAME, CONFIG_W_NAMES,
    C_MODEL, C_STUDY_GROUP, C_TEMPERATURE, C_RECS, C_LANGUAGE, C_PROMPT_TYPE, C_PROMPT_PARAM, C_STEM_MAGNITUDE,
    C_LIST_SSD,
)


def main(
        list_models: List[str],
        list_lang: List[str],
        list_prompt_types: List[str],
        list_prompt_params: List[str],
        list_temperatures: List[float],
) -> None:
    """
    Given a list of models, languages, prompt types, parameters, and temperature values, this method iterates through
    the recommendations provided by each model and prompt (each prompt is identified by prompt_type, prompt_params_file,
    and temperature). For each, it computes the STEM magnitude, the SSD coordinates, and collects the recommendations.
    It stores the computed values in a pandas DataFrame, which is saved in the `data/processed_output` folder.
    :param list_models: List of model names to process
    :param list_lang: list of Languages  to process
    :param list_prompt_types: List of prompt types to process
    :param list_prompt_params: List of prompt_params (e.g., CONFIG_NO_NAME) to process
    :param list_temperatures: List of temperature values to process
    :return: None
    """
    output_df = pd.DataFrame(
        columns=[C_MODEL, C_LANGUAGE, C_PROMPT_TYPE, C_PROMPT_PARAM, C_TEMPERATURE, C_STUDY_GROUP, C_STEM_MAGNITUDE]
                + C_LIST_SSD + [C_RECS]
    )
    for model in list_models:
        for lang in list_lang:
            for prompt_type in list_prompt_types:
                for prompt_params in list_prompt_params:
                    for temp in list_temperatures:
                        # Get the recommendations for the given model and prompt and iterate over them.
                        # TODO: I might actually make a method for this.
                        folder_path = os.path.join('data', 'processed_output', f'{prompt_type}', f'{lang}')
                        df = pd.read_csv(os.path.join(folder_path, f'responses_{model}_{lang}_{prompt_params}_temp_{temp}.csv'))

                        for index, (_, row) in enumerate(df.iterrows()):
                            # skip the recommendations if there are issues with it.
                            if to_be_skipped_due_to_empty_recommendation(row):
                                print(f"[INFO] Skipping item at index {index}, due to empty recommendation.")
                                continue

                            new_row_dict = {
                                    C_MODEL: [model],
                                    C_LANGUAGE: [lang],
                                    C_PROMPT_TYPE: [prompt_type],
                                    C_PROMPT_PARAM: [prompt_params],
                                    C_TEMPERATURE: [temp],
                                }

                            # get the target study group
                            target_study_group = get_target_dict_from_df_row(row)
                            new_row_dict[C_STUDY_GROUP] = [target_study_group]

                            # Compute STEM magnitude of the recommendation.
                            # TODO make a method for this
                            stem_magnitude = bool(row.is_stem_rec_0) * 5 + bool(row.is_stem_rec_1) * 4 \
                                             + bool(row.is_stem_rec_2) * 3 + bool(row.is_stem_rec_3) * 2 \
                                             + bool(row.is_stem_rec_4) * 1
                            new_row_dict[C_STEM_MAGNITUDE] = [stem_magnitude]

                            # Compute S.S.D. coordinates of the recommendation.
                            # TODO make a method for this
                            coordinate = np.zeros(14)
                            coordinate[int(row.ssd_rec_0) - 1] += 5
                            # I need "-1" because the ssd (stored in the DF) are in ['01'; '14'].
                            coordinate[int(row.ssd_rec_1) - 1] += 4
                            coordinate[int(row.ssd_rec_2) - 1] += 3
                            coordinate[int(row.ssd_rec_3) - 1] += 2
                            coordinate[int(row.ssd_rec_4) - 1] += 1
                            for idx in range(14):
                                new_row_dict[C_LIST_SSD[idx]] = [coordinate[idx]]

                            # To store the recs in a single column (just so it's easier to move them around).
                            new_row_dict[C_RECS] = [[row.rec_0, row.rec_1, row.rec_2, row.rec_3, row.rec_4]]

                            # Add the new row to the output dataframe.
                            new_row_df = pd.DataFrame(new_row_dict)
                            if len(output_df) == 0:
                                output_df = new_row_df.copy()
                            else:
                                output_df = pd.concat([output_df, new_row_df], ignore_index=True)

    output_df.to_csv(os.path.join('data', 'processed_output', 'stem_magnitude_ssd_coordinates_recs.csv'), index=False)


LIST_MODELS = MODELS_LIST
LIST_LANG = [IT]
LIST_PROMPT_TYPES = [USER_AS_STUDENT, LLM_AS_STUDENT, THIRD_PERSON_AS_STUDENT]
LIST_PROMPT_PARAMS = [CONFIG_NO_NAME, CONFIG_W_NAMES]
LIST_TEMPERATURES = [0.0, 0.3, 0.6]
if __name__ == '__main__':
    main(LIST_MODELS, LIST_LANG, LIST_PROMPT_TYPES, LIST_PROMPT_PARAMS, LIST_TEMPERATURES)
