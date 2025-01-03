# Languages
IT = 'it'
FR = 'fr'
EN = 'en'

# Params for the experiments
USER_AS_STUDENT = 'user_as_student'
LLM_AS_STUDENT = 'llm_as_student'
FRIEND_AS_STUDENT = 'friend_as_student'

CONFIG_NO_NAME = 'no_name'
CONFIG_W_NAMES = 'with_names'
CONFIG_NO_NAME_W_PRONOUNS = 'no_name_with_pronouns'

# Names, adjectives and nouns for the different languages
#     Italian names are taken from ISTAT
#     French names are taken from INSEE (https://www.insee.fr/fr/statistiques/3532172)
#     UK (eng + wales) names are from the ONS (gov.uk) -- stats from 2022:
#       https://www.ons.gov.uk/releases/babynamesinenglandandwales2022
#     US names are from SSA (Social Security Administration) -- stats from the 2010s: https://www.ssa.gov/
NAMES_F_IT = ['Sofia', 'Aurora', 'Giulia', 'Ginevra', 'Vittoria', 'Beatrice', 'Alice', 'Ludovica', 'Emma', 'Matilde']
NAMES_F_FR = ['Louise', 'Ambre', 'Alba', 'Jade', 'Emma', 'Rose', 'Alma', 'Alice', 'Romy', 'Anna']
NAMES_F_EN_UK = ['Olivia', 'Amelia', 'Isla', 'Ava', 'Lily', 'Ivy', 'Freya', 'Florence', 'Isabella', 'Sienna']
NAMES_F_EN_US = ['Emma', 'Olivia', 'Sophia', 'Isabella', 'Ava', 'Mia', 'Abigail', 'Emily', 'Charlotte', 'Madison']

NAMES_M_IT = ['Leonardo', 'Francesco', 'Tommaso', 'Edoardo', 'Alessandro', 'Lorenzo', 'Mattia', 'Gabriele', 'Riccardo', 'Andrea']
NAMES_M_FR = ['Gabriel', 'Raphaël', 'Léo', 'Louis', 'Maël', 'Noah', 'Jules', 'Adam', 'Arthur', 'Isaac']
NAMES_M_EN_UK = ['Noah', 'Muhammad', 'George', 'Oliver', 'Leo', 'Arthur', 'Oscar', 'Theodore', 'Theo', 'Freddie']
NAMES_M_EN_US = ['Noah', 'Liam', 'Jacob', 'William', 'Mason', 'Ethan', 'Michael', 'Alexander', 'James', 'Elijah']

NAMES_F = {
    IT: NAMES_F_IT,
    FR: NAMES_F_FR,
    EN: NAMES_F_EN_UK,
}
NAMES_M = {
    IT: NAMES_M_IT,
    FR: NAMES_M_FR,
    EN: NAMES_M_EN_UK,
}
ADJECTIVES_M = {
    IT: {'indeciso'},
    FR: {'indécis'},
    EN: {},
}
ADJECTIVES_F = {
    IT: {'indecisa'},
    FR: {'indécise'},
    EN: {},
}
ADJECTIVES_X = {
    IT: {'indecisə', 'indecis*'},
    FR: {'indécis·e'},
    EN: {'undecided'},
}
NOUNS_M = {
    IT: {'uno studente'},
    FR: {'un étudiant'},
    EN: {},
}
NOUNS_F = {
    IT: {'una studentessa'},
    FR: {'une étudiante'},
    EN: {},
}
NOUNS_X = {
    IT: {'unə studentə', 'un* student*'},
    FR: {'un·e étudiant·e'},
    EN: {'a student'},
}

# Models
GPT_3_5 = 'gpt_3_5'
GPT_4o_MINI = 'gpt_4o_mini'
GPT_4o = 'gpt_4o_mini'
# Not implemented for now.
# GPT_o1_mini = 'gpt_o1_mini'
# GPT_o1 = 'gpt_o1'

OPENAI_MODEL_TO_API_NAME = {
    GPT_3_5: 'gpt-3.5-turbo-0125',
    GPT_4o_MINI: 'gpt-4o-mini-2024-07-18',  # Default as of 18 December 2024
    GPT_4o: 'gpt-4o-2024-08-06',            # Default as of 18 December 2024
    # GPT_o1_mini: 'o1-mini-2024-09-12',      # Default as of 18 December 2024
    # GPT_o1: 'o1-2024-12-17',                # Default as of 18 December 2024
}

CLAUDE_3_5_SONNET = 'claude_3_5_sonnet'
CLAUDE_3_5_HAIKU = 'claude_3_5_haiku'
ANTHROPIC_MODEL_TO_API_NAME = {
    CLAUDE_3_5_SONNET : 'claude-3-5-sonnet-20241022',
    CLAUDE_3_5_HAIKU: 'claude-3-5-haiku-20241022',
}

GEMINI_1_5_FLASH = 'gemini_1_5'
GEMINI_1_5_FLASH_8B = 'gemini_1_5_8b'
GOOGLE_MODEL_TO_API_NAME = {
    GEMINI_1_5_FLASH: 'gemini-1.5-flash',
    GEMINI_1_5_FLASH_8B: 'gemini-1.5-flash-8b',
}

GEMMA_2B = 'gemma_2b'
GEMMA_7B = 'gemma_7b'
LLAMA_3_8B = 'llama3_8b'
LLAMA_3_2_1B = 'llama3_2_1b'
# LLAMA_3_1_8B = 'llama3_1_8b'
# MISTRAL_7B_v02 = 'mistral_v02_7b'
# MISTRAL_7B_v03 = 'mistral_v03_7b'
HUGGINGFACE_MODEL_NAMES = {
    GEMMA_2B: "google/gemma-2b-it",
    GEMMA_7B: "google/gemma-7b-it",
    LLAMA_3_8B: "meta-llama/Meta-Llama-3-8B-Instruct",
    LLAMA_3_2_1B: "meta-llama/Llama-3.2-1B-Instruct",
    # LLAMA_3_1_8B: "meta-llama/Meta-Llama-3.1-8B-Instruct",
    # MISTRAL_7B_v02: "mistralai/Mistral-7B-Instruct-v0.2",
    # MISTRAL_7B_v03: "mistralai/Mistral-7B-Instruct-v0.3",
}
