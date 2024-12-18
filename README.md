# Evaluation of bias in LLM-based degree recomendations

## How to use
To run the experiments with the models and configuration parameters already defined in this repo, it is sufficient to 
set the desired parameters in the `01_main_perform_recs.py` script and run it.

For instance, you should set (in `main` in `01_main_perform_recs.py`):
```python
    LANGUAGE = IT
    MODEL = GPT_4o_MINI
    N_RUNS_PER_PROMPT = 10
    TEMPERATURE = 0.0  # in [0.0, 0.3, 0.6]
    PROMPT_PARAMS_FILE = CONFIG_NO_NAME  # For experiments without names
    PROMPT_TYPE = USER_AS_STUDENT        # For experiments with the "user as student" type of prompts.
```
The code produces one output file:
```
"data/output/{PROMPT_TYPE}/{LANGUAGE}/responses_{MODEL}_{LANGUAGE}_{PROMPT_PARAMS_FILE}_temp_{TEMPERATURE}.csv"
```
with the responses from the LLM.

Please note that the code takes the API keys from environment variables, using `os.environ.get(key_name)`, thus you 
should do like `export OPENAI_KEY=<you-API-key>` (for the model you want to use) before running the script.

## Repo structure
```
bias_in_edu_llms
│
├── config/  # Files with the params used to create the prompts.
│
├── data/
│   ├── interim/
│   ├── output/           # The LLM responses.
│   └── procesed_output/  # The LLM responses, after parsing them.
│
├── figures/
│
├── 00_script_prepare_params_files_for_experiments_with_names.py
│
├── 01_main_perform_recs.py  # Perform course recommendations with LLMs.
│
├── 02_parse_responses.py  # Collect the recommended courses.
│
├── constants.py  # Definition of parameters, models, etc.
│
├── course_mappings.py  # For merging different wordings of the same course.
│
├── prompts_friend_as_student.py  # List of prompt templates.
├── prompts_llm_as_student.py     # List of prompt templates.
├── prompts_user_as_student.py    # List of prompt templates.
│
├── regex_patterns.py  # Regex used to parse the LLM responses.
│
├── utils.py
│
├── utils_anthropic.py  # Code to call the Anthropic API.
├── utils_google.py     # Code to call the Google AI API.
├── utils_keys.py       # Management of API keys.
├── utils_open_ai.py    # Code to call the OpenAI API.
│
└── utils_parsing.py    # Util methods for parsing the LLM respones.
```
