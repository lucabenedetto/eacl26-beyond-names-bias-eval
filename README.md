# Evaluation of bias in LLM-based degree recomendations

## How to use
To run the experiments with the models and configuration parameters already defined in this repo, it is sufficient to 
set the desired parameters in the `01_main_perform_recs.py` script and run it.

For instance, you should set (in `main` in `01_main_perform_recs.py`):
```python
LANGUAGE = IT
MODEL = GPT_4o_MINI
N_RUNS_PER_PROMPT = 10
TEMPERATURE = 0.0                    # in [0.0, 0.3, 0.6]
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
Currently, the code manages the following keys: `OPENAI_KEY`, `ANTHROPIC_KEY`, `GOOGLE_AI_KEY`.
Which one to pick is chosen depending on the model name; if you add new models, you should also update the 
`get_api_key_from_model` method (or the constants used in it) in `utils_keys.py` as needed.

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
├── figures/  # Figures created with the analysis scripts are stored here.
│
├── 00_script_prepare_params_files_for_experiments_with_names.py
│
├── 01_main_perform_recs.py       # Perform course recommendations with LLMs.
│
├── 02_parse_responses.py         # Collect the recommended courses.
│
├── 03_1_compute_stem_magnitude_and_ssd_coordinates.py          # Takes the (parsed recommendations and computes the STEM Magnitude and SSD Coordinates of the recommendations.
├── 03_2_pca_reduction_ssd_coordinates.py                       # Reduces the SSD Coordinates with PCA.
├── 03_2_tsne_reduction_ssd_coordinates.py                      # Reduces the SSD Coordinates with t-SNE (not used in the paper).
├── 03_3_analysis_pca_components.py                             # Performs the analysis of the PCA model trained in 03_2_pca_reduction_ssd_coordinates.py
├── 03_3_compute_max_emd.py                                     # Computes the maximum EMD (Earth Mover's Distance) that might be observed in the data if all the points were at max_x, max_y and min_x, min_y in the PCA reduced space.
├── 03_3_full_run_analysis_pca_reduced_ssd_coordinates.py       # Runs all the analysis whose results are shown in the paper (SSD Coordinates).
├── 03_3_full_run_analysis_stem_magnitude_of_recommendations.py # Runs all the analysis whose results are shown in the paper (STEM Magnitude).
│
├── constants.py                  # Definition of parameters, models, etc.
│
├── course_mappings.py            # For merging different wordings of the same course.
│
├── prompts_llm_as_student.py     # List of prompt templates for the first person setting.
├── prompts_user_as_student.py    # List of prompt templates for the second person setting.
├── prompts_third_as_student.py   # List of prompt templates for the third person setting.
│
├── regex_patterns.py             # Regex used to parse the LLM responses.
│
├── utils.py                      # Misc. utils methods.
│
├── utils_anthropic.py            # Code to call the Anthropic API.
├── utils_google.py               # Code to call the Google AI API.
├── utils_keys.py                 # Management of API keys.
├── utils_open_ai.py              # Code to call the OpenAI API.
│
└── utils_parsing.py              # Util methods for parsing the LLM respones.
```
