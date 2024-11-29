# Italian names are taken from ISTAT
# French names are taken from INSEE (https://www.insee.fr/fr/statistiques/3532172)
NAMES_F_IT = ['Sofia', 'Aurora', 'Giulia', 'Ginevra', 'Vittoria', 'Beatrice', 'Alice', 'Ludovica', 'Emma', 'Matilde']
NAMES_F_FR = ['Louise', 'Ambre', 'Alba', 'Jade', 'Emma', 'Rose', 'Alma', 'Alice', 'Romy', 'Anna']

NAMES_M_IT = ['Leonardo', 'Francesco', 'Tommaso', 'Edoardo', 'Alessandro', 'Lorenzo', 'Mattia', 'Gabriele', 'Riccardo', 'Andrea']
NAMES_M_FR = ['Gabriel', 'Raphaël', 'Léo', 'Louis', 'Maël', 'Noah', 'Jules', 'Adam', 'Arthur', 'Isaac']

IT = 'it'
FR = 'fr'
EN = 'en'

GPT_3_5 = 'gpt_3_5'
GPT_4o_MINI = 'gpt_4o_mini'

OPENAI_MODEL_TO_API_NAME = {
    GPT_3_5: 'gpt-3.5-turbo-0125',
    GPT_4o_MINI: 'gpt-4o-mini',
}

CLAUDE_3_5 = 'claude_3_5_sonnet'
ANTHROPIC_MODEL_TO_API_NAME = {
    CLAUDE_3_5 : 'claude-3-5-sonnet-20241022',
}

GEMINI_1_5_FLASH = 'gemini_1_5'
GEMINI_1_5_FLASH_8B = 'gemini_1_5_8b'
GOOGLE_MODEL_TO_API_NAME = {
    GEMINI_1_5_FLASH: 'gemini-1.5-flash',
    GEMINI_1_5_FLASH_8B: 'gemini-1.5-flash-8b',
}
