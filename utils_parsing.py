import re
from typing import List, Optional
from constants import (
    IT, FR, EN,
    GPT_3_5, GPT_4o_MINI, GPT_4o, GPT_4_1_NANO,
    CLAUDE_3_5_SONNET, CLAUDE_3_5_HAIKU,
    GEMINI_1_5_FLASH_8B, GEMINI_1_5_FLASH, GEMINI_2_5_FLASH_LITE,
)
from regex_patterns import REGEX_PATTERNS


def clean_parsed_responses(parsed_response, model, language):
    clean_texts = [clean_single_text(x, model, language) for x in parsed_response]
    if model in {GEMINI_2_5_FLASH_LITE}:
        # This is to avoid things such as:
        #  = "perché considerarla"
        clean_texts = [x for x in clean_texts if x != "perché considerarla"]
        clean_texts = [x for x in clean_texts if x != "perché considerarlo"]
        clean_texts = [x for x in clean_texts if x != "sfide"]
    if model in {GEMINI_1_5_FLASH_8B}:
        # This is needed to avoid things such as:
        #  - "['quali sono i tuoi interessi?']"
        #  - "nel frattempo, ecco 5 corsi di laurea in diverse aree, come esempio generico"
        clean_texts = [x for x in clean_texts if x[-1] != '?']
        clean_texts = [x for x in clean_texts if x[:9] != "invece di"]
        clean_texts = [x for x in clean_texts if x[:13] != "in assenza di"]
        clean_texts = [x for x in clean_texts if x[:14] != "nel frattempo,"]
        clean_texts = [x for x in clean_texts if x[:8] != "per ora,"]
        clean_texts = [x for x in clean_texts if x[:33] != "in attesa di queste informazioni,"]
        clean_texts = [x for x in clean_texts if x[:15] != "in alternativa,"]
        info_request_keywords = {
            'interessi', 'competenze', 'ambizioni', 'aspetti pratici', 'possibili',
            'i suoi interessi', 'le sue abilità', 'le sue aspirazioni future', 'le sue esigenze',
            'parlare con lui', 'esplorare i contenuti dei corsi', 'considerare le sue abilità',
            'valutare le prospettive di lavoro',

        }
        clean_texts = [x for x in clean_texts if x not in info_request_keywords]
    return clean_texts


def truncate_and_keep_first(text: str, literals: List[str]) -> str:
    for literal in literals:
        text = text.split(literal)[0]
    text = text.strip()
    return text


def clean_single_text(text, model, language):
    # Remove blank spaces at the beginning/end and make everything lowercase.
    text = text.strip().lower()
    # Remove parentheses from the name of the degree.
    if '(' in text and ')' in text:
        text = re.sub(r'\([^()]*\)', ' ', text)
        text = text.strip()
    # Some models do not respond only with the name of the course but also by adding "Degree in..." (in different lang).
    if model in {GPT_3_5, GPT_4o_MINI, GPT_4o, GPT_4_1_NANO, GEMINI_1_5_FLASH_8B, CLAUDE_3_5_HAIKU}:
        if text[:10] == "laurea in ":
            text = text[10:]
    if model == GPT_4o:
        text = truncate_and_keep_first(text, literals=[
            ":",  # KeyError: 'ingegneria informatica:'
        ])
    if model == GPT_4_1_NANO:
        text = truncate_and_keep_first(text, literals=[
            ' – percorso',
            ', come '
        ])
        text = text.replace('’', "'")
        text = text.replace('   ', " ")
        text = text.replace(" o ", "/")
        text = text.replace(" / ", "/")
        text = text.replace(", ", "/")
        # text = text.replace(" e ", "/")
        text = text.replace(" - ", "/")
    if model == GPT_3_5:
        text = truncate_and_keep_first(text, literals=[
            ": ",  # KeyError: "ingegneria informatica: se sei interessata alla tecnologia, all'informatica e alla risoluzione di problemi complessi, potresti valutare questo corso di laurea che ti permetterà di acquisire competenze nel campo dell'ingegneria informatica."
            "\n",  # KeyError: 'lingue e letterature straniere\n\nquesti sono solo alcuni esempi, assicurati di esplorare diverse opzioni e scegliere un corso di laurea che ti appassioni e che sia in linea con i tuoi interessi e obiettivi di carriera. buona fortuna nella tua scelta!'
        ])
    if model in {GEMINI_1_5_FLASH_8B}:
        if text[-1] == '.':
            text = text[:-1]
        if text[:21] == "laurea magistrale in ":
            text = text[21:]
        text = text.split(" - ")[0]
    if model == GEMINI_1_5_FLASH_8B:
        text = truncate_and_keep_first(text, literals=[
            ', con specializzazione',
            ', specializzazione',
            ', indirizzo',
            ', università ',
            ', politecnico',
        ])
    if model == GEMINI_2_5_FLASH_LITE:
        text = truncate_and_keep_first(text, literals=[
            " (con specializzazione in",
            " (con indirizzi in",
        ])
        text = text.replace(" / ", "/")
    if model == CLAUDE_3_5_HAIKU:
        text = truncate_and_keep_first(text, literals=[
            ": ",
            " - ",
            ", per",  # e.g. "design, per unire la mia creatività con competenze tecniche moderne"
            " all'università ",  # e.g.: "psicologia all'università di bologna"
            " alla sapienza di roma",
            " alla bocconi di milano",
            " al politecnico ",
            " del politecnico",
            " presso l'università",
            " con indirizzo",
            ", visto che",
        ])
    if model == CLAUDE_3_5_SONNET:
        text = truncate_and_keep_first(text, literals=[
            " - ",
            ": ",
            ", perché",  # e.g. ingegneria informatica, perché mi appassionano la tecnologia e la programmazione e offre ottime prospettive lavorative
            ", dato che",
            " dato che",
            ", che",
            ", in quanto",
            " in quanto",
            ", poiché",
            " poiché",
            " perché ",
            " al politecnico ",
            " presso il politecnico ",
            " all'università ",  # e.g.: "economia e management all'università bocconi"
            " alla ",  # e.g.: "alla iulm di milano", "alla sapienza di Roma", "alla naba di milano"
            ", visto che",
            ", per la",
            ", dato il",  # e.g.: , "dato il mio interesse per la politica e gli affari globali"
        ])

    return text


def parse_with_multiple_patterns(text, patterns):
    # NB: the order of the patterns is relevant!!
    for pattern in patterns:
        match = re.findall(pattern, text)
        if match:
            return match
    # "/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\"
    print("/\\"*20, "\n", text, "/\\"*20, "\n")  # print the text if it didn't match any regex
    return None


def parse_llm_response(response: str, model: str, language: str) -> Optional[List[str]]:
    # Parse response with the pattern(s) defined in the regex_patterns.py file.
    parsed_response = parse_with_multiple_patterns(response, REGEX_PATTERNS[model])
    if parsed_response is None:
        return None
    # Perform the additional cleaning for the models that need it.
    parsed_response = clean_parsed_responses(parsed_response, model, language)
    return parsed_response
