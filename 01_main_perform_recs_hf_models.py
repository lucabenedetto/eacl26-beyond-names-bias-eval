import os
import pandas as pd
from datasets import Dataset

from src.huggingface_llm_recommender import HuggingFaceLLMRecommender
from utils import get_llm_response
from utils_keys import get_api_key_from_model
from constants import (
    IT, FR, EN,
    GPT_3_5, GPT_4o_MINI, GPT_4o,
    CLAUDE_3_5_SONNET, CLAUDE_3_5_HAIKU,
    GEMINI_1_5_FLASH_8B, GEMINI_1_5_FLASH,
    LLAMA_3_2_1B,
    GEMMA_2B,
    GEMMA_7B,
    GEMMA_2_2B,
    GEMMA_2_9B,
    LLAMA_3_8B,
    LLAMA_3_2_1B,
    LLAMA_3_2_3B,
    OLMO_2_7B,
    OLMO_2_13B,
    SMOLLM2_135M,
    SMOLLM2_360M,
    HUGGINGFACE_MODEL_NAMES,
    USER_AS_STUDENT, LLM_AS_STUDENT,
    FRIEND_AS_STUDENT,
    CONFIG_NO_NAME,
    CONFIG_W_NAMES,
    CONFIG_NO_NAME_W_PRONOUNS,
)
from prompts_friend_as_student import get_prompt_friend_as_student
from prompts_user_as_student import get_prompt_user_as_student
from prompts_llm_as_student import get_prompt_llm_as_student


def main(model_name, language, prompt_type, prompt_params_file, temperature=0.0, n_runs_per_prompt=1):
    # Each output file contains all the results for one temperature value and one model
    # Also, the script produces one file for the results with names and one for all the results without the names.

    if prompt_type not in {USER_AS_STUDENT, LLM_AS_STUDENT, FRIEND_AS_STUDENT}:
        raise ValueError('Invalid prompt_type')
    # TODO add check for prompt type and prompt params file so that they don't are incompatible (e.g. FRIEND AS STUDENT
    #   with prompt type without pronouns.

    api_key = get_api_key_from_model(model_name)

    out_df = pd.DataFrame(columns=['language', 'model', 'response', 'with_name', 'with_noun', 'with_adjective',
                                   'with_pronouns',
                                   'name', 'noun', 'adjective',
                                   'pronoun_0', 'pronoun_1', 'pronoun_2', 'pronoun_3', 'pronoun_4',
                                   'ending_id', 'n_uni_courses', 'prompt', 'temperature'])

    # if model_name in HUGGINGFACE_MODEL_NAMES:
    recommender = HuggingFaceLLMRecommender(model_name=model_name, access_token=api_key)  #, use_gpu=True)  # TODO: make param for use_gpu
    # else:
    #     # TODO: I will upload the code to have Recommender objects for API-based models too.
    #     recommender = None

    prompt_params_df = pd.read_csv(os.path.join('config', f'params_{prompt_params_file}_{language}.csv'))

    # Prepare the input dataset.
    list_user_prompts = []
    for row in prompt_params_df.itertuples():
        if prompt_type == USER_AS_STUDENT:
            prompt = get_prompt_user_as_student(language=language, name=row.name, noun=row.noun, adjective=row.adjective, n_uni_courses=row.n_uni_courses)
        elif prompt_type == FRIEND_AS_STUDENT:
            prompt = get_prompt_friend_as_student(
                language=language,
                name=row.name,
                noun=row.noun,
                adjective=row.adjective,
                pronouns=(row.pronoun_0, row.pronoun_1, row.pronoun_2, row.pronoun_3, row.pronoun_4),
                n_uni_courses=row.n_uni_courses,
            )
        else:  # prompt_type == LLM_AS_STUDENT
            prompt = get_prompt_llm_as_student(language=language, name=row.name, noun=row.noun, adjective=row.adjective, n_uni_courses=row.n_uni_courses)
        print(f"[INFO] {prompt}")
        for _ in range(n_runs_per_prompt):
            list_user_prompts.append(prompt)  # This is to have multiple runs with the same prompt.

    # run the on the whole dataset
    # if model_name in HUGGINGFACE_MODEL_NAMES:
    list_responses = recommender.perform_recommendation_whole_dataset(user_prompts=list_user_prompts, temperature=temperature)
    # else:
    #     response = get_llm_response(api_key, model_name, prompt, temperature)

    # build the output df
    idx = 0
    for row in prompt_params_df.itertuples():
        for _ in range(n_runs_per_prompt):
            new_row_df = pd.DataFrame({
                'language': [language],
                'model': [model_name],
                'response': [list_responses[idx]],
                'with_name': [row.with_name],
                'with_noun': [row.with_noun],
                'with_adjective': [row.with_adjective],
                'with_pronouns': [row.with_adjective],
                'name': [row.name],
                'noun': [row.noun],
                'adjective': [row.adjective],
                'pronoun_0': [row.pronoun_0],
                'pronoun_1': [row.pronoun_1],
                'pronoun_2': [row.pronoun_2],
                'pronoun_3': [row.pronoun_3],
                'pronoun_4': [row.pronoun_4],
                'ending_id': [row.ending_id],
                'n_uni_courses': [row.n_uni_courses],
                'prompt': [list_responses[idx]],
                'temperature': [temperature],
            })
            idx += 1
            if len(out_df) == 0:
                out_df = new_row_df.copy()
            else:
                out_df = pd.concat([out_df, new_row_df], ignore_index=True)

    # save the output df
    folder_path = os.path.join('data', 'output', f'{prompt_type}', f'{language}')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"[INFO] Created folder {folder_path}")
    else:
        print(f"[INFO] Folder already exists: {folder_path}")
    out_df.to_csv(os.path.join(folder_path, f'responses_{model_name}_{language}_{prompt_params_file}_temp_{temperature}.csv'), index=False)


if __name__ == '__main__':
    # Params to set:
    LANGUAGE = FR
    MODEL = SMOLLM2_360M
    N_RUNS_PER_PROMPT = 10  # 10
    # TEMPERATURE = 0.0  # in [0.0, 0.3, 0.6]

    PROMPT_PARAMS_FILE = CONFIG_NO_NAME  # For experiments without names
    # PROMPT_PARAMS_FILE = CONFIG_W_NAMES  # For experiments with names
    # PROMPT_PARAMS_FILE = CONFIG_NO_NAME_W_PRONOUNS  # For experiments with pronouns without names

    # PROMPT_TYPE = USER_AS_STUDENT
    # PROMPT_TYPE = LLM_AS_STUDENT
    # PROMPT_TYPE = FRIEND_AS_STUDENT

    for PROMPT_TYPE in [USER_AS_STUDENT]:  # , LLM_AS_STUDENT]:
        for TEMPERATURE in [0.01]:  # , 0.3, 0.6]:
            main(MODEL, LANGUAGE, PROMPT_TYPE, PROMPT_PARAMS_FILE, temperature=TEMPERATURE, n_runs_per_prompt=N_RUNS_PER_PROMPT)
