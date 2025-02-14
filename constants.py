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
GPT_4o = 'gpt_4o'

OPENAI_MODEL_TO_API_NAME = {
    GPT_3_5: 'gpt-3.5-turbo-0125',
    GPT_4o_MINI: 'gpt-4o-mini-2024-07-18',  # Default as of 18 December 2024
    GPT_4o: 'gpt-4o-2024-08-06',            # Default as of 18 December 2024
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

# These are the models evaluated in the experiments for the ARR paper (target EMNLP).
MODELS_LIST = [
    GPT_3_5,
    GPT_4o_MINI,
    GPT_4o,
    CLAUDE_3_5_SONNET,
    CLAUDE_3_5_HAIKU,
    GEMINI_1_5_FLASH,
    GEMINI_1_5_FLASH_8B,
]

MODELS_BY_OWNER = {
    'OpenAI': {GPT_3_5, GPT_4o_MINI, GPT_4o},
    'Anthropic': {CLAUDE_3_5_SONNET, CLAUDE_3_5_HAIKU},
    'Google': {GEMINI_1_5_FLASH, GEMINI_1_5_FLASH_8B},
}


# Column names
C_MODEL = 'model'
C_LANGUAGE = 'language'
C_PROMPT_TYPE = 'prompt_type'
C_PROMPT_PARAM = 'prompt_param'
C_TEMPERATURE = 'temperature'
C_STUDY_GROUP = 'study_group'
C_STEM_MAGNITUDE = 'STEM_magnitude'
C_RECS = 'recommendations'
C_PCA_0 = 'pca_0'
C_PCA_1 = 'pca_1'

C_LIST_SSD = [f'SSD_{i}' for i in range(14)]
