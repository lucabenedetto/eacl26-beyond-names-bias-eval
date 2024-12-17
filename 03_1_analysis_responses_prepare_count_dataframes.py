import os
import pandas as pd

import matplotlib.pyplot as plt

from constants import (
    IT, FR, EN,
    GPT_3_5, GPT_4o_MINI,
    CLAUDE_3_5_SONNET, CLAUDE_3_5_HAIKU,
    GEMINI_1_5_FLASH_8B, GEMINI_1_5_FLASH,
    USER_AS_STUDENT, LLM_AS_STUDENT,
)


def main(language):
    # create one DF where each row counts the number of mentions of a course for each param configuration.
    out_df = pd.DataFrame(columns=['model', 'prompt_type', 'prompt_params_file', 'temperature', 'course', 'count'])
    # Iterate over all the models, prompt types and parameters
    for model in [GPT_3_5, GPT_4o_MINI, CLAUDE_3_5_HAIKU, GEMINI_1_5_FLASH, GEMINI_1_5_FLASH_8B]:
        for prompt_type in [USER_AS_STUDENT, LLM_AS_STUDENT]:
            for prompt_params_file in ['with_names', 'no_name']:
                for temperature in [0.0, 0.3, 0.6]:
                    # Load DF with the parsed responses.
                    folder_path = os.path.join('data', 'processed_output', f'{prompt_type}', f'{language}')
                    df = pd.read_csv(os.path.join(folder_path, f'responses_{model}_{language}_{prompt_params_file}_temp_{temperature}.csv'))

                    groupby_dfs = [
                        df.groupby(f'rec_{idx}').size().reset_index().sort_values(0, ascending=False).rename(columns={f'rec_{idx}': 'rec'})
                        for idx in range(5)
                    ]
                    count_dict = {}
                    for groupby_df in groupby_dfs:
                        for course, count in groupby_df[['rec', 0]].values:
                            if course not in count_dict:
                                count_dict[course] = count
                            else:
                                count_dict[course] += count

                    # print(count_dict)
                    total_count_df = pd.DataFrame.from_dict(count_dict, orient='index').sort_values(0).reset_index()
                    total_count_df['model'] = model
                    total_count_df['prompt_type'] = prompt_type
                    total_count_df['prompt_params_file'] = prompt_params_file
                    total_count_df['temperature'] = temperature
                    total_count_df = total_count_df.rename(columns={0: 'count', 'index': 'course'})
                    if len(out_df) == 0:
                        out_df = total_count_df.copy()
                    else:
                        out_df = pd.concat([out_df, total_count_df], ignore_index=True)
    out_df.to_csv(f'data/interim/count_recommended_courses_by_config_{language}.csv', index=False)

    # Same as above but separately for each model.
    for model in [GPT_3_5, GPT_4o_MINI, CLAUDE_3_5_HAIKU, GEMINI_1_5_FLASH, GEMINI_1_5_FLASH_8B]:
        local_df = out_df[out_df['model'] == model]
        # print(local_df)
        local_df = local_df.groupby('course')['count'].sum().reset_index().sort_values('count', ascending=False)
        # print(local_df)
        local_df.to_csv(f'data/interim/count_recommended_courses_aggregate_{model}_{language}.csv', index=False)


if __name__ == '__main__':
    # Params to set:
    LANGUAGE = IT
    # MODEL = GPT_3_5

    # for PROMPT_PARAMS_FILE in ['with_names', 'no_name']:
    #     for PROMPT_TYPE in [USER_AS_STUDENT, LLM_AS_STUDENT]:
    #         for TEMPERATURE in [0.0, 0.3, 0.6]:
    #             print(f"[INFO] Doing Model {MODEL} | Language {IT} | Temperature {TEMPERATURE} | Prompt type {PROMPT_TYPE} | Prompt params file {PROMPT_PARAMS_FILE}.")
    #             main(MODEL, LANGUAGE, PROMPT_TYPE, PROMPT_PARAMS_FILE, temperature=TEMPERATURE)

    # PROMPT_PARAMS_FILE = 'with_names'
    # PROMPT_TYPE = LLM_AS_STUDENT
    # TEMPERATURE = 0.3
    # print(f"[INFO] Doing Model {MODEL} | Language {IT} | Temperature {TEMPERATURE} | Prompt type {PROMPT_TYPE} | Prompt params file {PROMPT_PARAMS_FILE}.")
    main(LANGUAGE)
