# Evaluation of bias in LLM-based degree recomendations

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
