import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils import get_llm_response
from utils_keys import get_api_key_from_model
from constants import (
    IT, FR, EN,
    GPT_3_5, GPT_4o_MINI, GPT_4o,
    CLAUDE_3_5_SONNET, CLAUDE_3_5_HAIKU,
    CLAUDE_4_SONNET,
    GEMINI_1_5_FLASH_8B, GEMINI_1_5_FLASH,
    USER_AS_STUDENT, LLM_AS_STUDENT,
    THIRD_PERSON_AS_STUDENT,
    CONFIG_NO_NAME,
    CONFIG_W_NAMES,
)
from prompts_third_person_as_student import get_prompt_third_person_as_student
from prompts_user_as_student import get_prompt_user_as_student
from prompts_llm_as_student import get_prompt_llm_as_student


def process_single_prompt(row, api_key, model, language, prompt_type, temperature, n_runs_per_prompt):
    """Process a single prompt row and return list of result dictionaries."""
    # Generate the prompt based on prompt type
    if prompt_type == USER_AS_STUDENT:
        prompt = get_prompt_user_as_student(language=language, name=row.name, noun=row.noun, adjective=row.adjective, n_uni_courses=row.n_uni_courses)
    elif prompt_type == THIRD_PERSON_AS_STUDENT:
        prompt = get_prompt_third_person_as_student(
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
    
    # Process all runs for this prompt
    results = []
    for _ in range(n_runs_per_prompt):
        response = get_llm_response(api_key, model, prompt, temperature)
        result_dict = {
            'language': language,
            'model': model,
            'response': response,
            'with_name': row.with_name,
            'with_noun': row.with_noun,
            'with_adjective': row.with_adjective,
            'with_pronouns': row.with_adjective,
            'name': row.name,
            'noun': row.noun,
            'adjective': row.adjective,
            'pronoun_0': row.pronoun_0,
            'pronoun_1': row.pronoun_1,
            'pronoun_2': row.pronoun_2,
            'pronoun_3': row.pronoun_3,
            'pronoun_4': row.pronoun_4,
            'ending_id': row.ending_id,
            'n_uni_courses': row.n_uni_courses,
            'prompt': prompt,
            'temperature': temperature,
        }
        results.append(result_dict)
    
    return results


def main(model, language, prompt_type, prompt_params_file, temperature=0.0, n_runs_per_prompt=1, max_workers=4):
    # Each output file contains all the results for one temperature value and one model
    # Also, the script produces one file for the results with names and one for all the results without the names.

    if prompt_type not in {USER_AS_STUDENT, LLM_AS_STUDENT, THIRD_PERSON_AS_STUDENT}:
        raise ValueError('Invalid prompt_type')
    # TODO add check for prompt type and prompt params file so that they don't are incompatible (e.g. FRIEND AS STUDENT
    #   with prompt type without pronouns.

    api_key = get_api_key_from_model(model)

    out_df = pd.DataFrame(columns=['language', 'model', 'response', 'with_name', 'with_noun', 'with_adjective',
                                   'with_pronouns',
                                   'name', 'noun', 'adjective',
                                   'pronoun_0', 'pronoun_1', 'pronoun_2', 'pronoun_3', 'pronoun_4',
                                   'ending_id', 'n_uni_courses', 'prompt', 'temperature'])

    # In the files available on github, the "params_{prompt_params_file}_{language}.csv" files are for 1st & 2nd person
    #   the "params_{prompt_params_file}_{language}_third_person.csv" for 3rd person only.
    if prompt_type in {USER_AS_STUDENT, LLM_AS_STUDENT}:
        prompt_params_df = pd.read_csv(os.path.join('config', f'params_{prompt_params_file}_{language}.csv'))
    else:  # prompt_type == THIRD_PERSON_AS_STUDENT
        prompt_params_df = pd.read_csv(os.path.join('config', f'params_{prompt_params_file}_{language}_third_person.csv'))

    # Collect all results from parallel execution
    all_results = []
    
    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_row = {
            executor.submit(process_single_prompt, row, api_key, model, language, prompt_type, temperature, n_runs_per_prompt): row
            for i, row in enumerate(prompt_params_df.itertuples()) if i < 10
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_row):
            try:
                results = future.result()
                all_results.extend(results)
            except Exception as exc:
                row = future_to_row[future]
                print(f'[ERROR] Row {row.Index} generated an exception: {exc}')
    
    # Convert all results to DataFrame
    if all_results:
        out_df = pd.DataFrame(all_results)
    else:
        out_df = pd.DataFrame(columns=['language', 'model', 'response', 'with_name', 'with_noun', 'with_adjective',
                                       'with_pronouns', 'name', 'noun', 'adjective',
                                       'pronoun_0', 'pronoun_1', 'pronoun_2', 'pronoun_3', 'pronoun_4',
                                       'ending_id', 'n_uni_courses', 'prompt', 'temperature'])

    folder_path = os.path.join('data', 'output', f'{prompt_type}', f'{language}')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"[INFO] Created folder {folder_path}")
    else:
        print(f"[INFO] Folder already exists: {folder_path}")
    out_df.to_csv(os.path.join(folder_path, f'responses_{model}_{language}_{prompt_params_file}_temp_{temperature}.csv'), index=False)


if __name__ == '__main__':
    # Params to set:
    LANGUAGE = IT
    MODELS = [CLAUDE_4_SONNET]
    N_RUNS_PER_PROMPT = 3  # 3 or 10 / For the paper, we use 3 for the experiments with names and 10 for the experiments without names.
    TEMPERATURES = [0.0, 0.3, 0.6]
    MAX_WORKERS = 4  # Number of parallel workers for concurrent execution

    # PROMPT_PARAMS_FILE = CONFIG_NO_NAME  # For experiments without names
    PROMPT_PARAMS_FILE = CONFIG_W_NAMES  # For experiments with names

    # PROMPT_TYPE = USER_AS_STUDENT
    # PROMPT_TYPE = LLM_AS_STUDENT
    PROMPT_TYPE = THIRD_PERSON_AS_STUDENT
    for MODEL in MODELS:
        for TEMPERATURE in TEMPERATURES:
            main(MODEL, LANGUAGE, PROMPT_TYPE, PROMPT_PARAMS_FILE, temperature=TEMPERATURE, n_runs_per_prompt=N_RUNS_PER_PROMPT, max_workers=MAX_WORKERS)
