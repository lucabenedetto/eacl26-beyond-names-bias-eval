import re
from typing import List, Optional
from constants import (
    IT, FR, EN,
    GPT_3_5, GPT_4o_MINI,
    CLAUDE_3_5_SONNET, CLAUDE_3_5_HAIKU,
    GEMINI_1_5_FLASH_8B, GEMINI_1_5_FLASH,
)
from regex_patterns import REGEX_PATTERNS
from course_mappings import COURSE_MAPPINGS_IT


def clean_parsed_responses(parsed_response, model, language):
    clean_texts = [clean_single_text(x, model, language) for x in parsed_response]
    if model in {GEMINI_1_5_FLASH_8B}:
        # This is needed to avoid things such as "['quali sono i tuoi interessi?']"
        clean_texts = [x for x in clean_texts if x[-1] != '?']
    return clean_texts


def clean_single_text(text, model, language):
    # Remove blank spaces at the beginning/end and make everything lowercase.
    text = text.strip().lower()
    # Remove parentheses from the name of the degree.
    if '(' in text and ')' in text:
        text = re.sub(r'\([^()]*\)', ' ', text)
        text = text.strip()
    # Some models do not respond only with the name of the course but also by adding "Degree in..." (in different lang).
    if model in {GPT_3_5, GPT_4o_MINI, GEMINI_1_5_FLASH_8B}:
        if text[:10] == "laurea in ":
            text = text[10:]
    if model in {GEMINI_1_5_FLASH_8B}:
        if text[-1] == '.':
            text = text[:-1]
        if text[:21] == "laurea magistrale in ":
            text = text[21:]
        text = text.split(" - ")[0]
    if model == GEMINI_1_5_FLASH_8B:
        text = text.split(', con specializzazione')[0]
        text = text.split(', specializzazione')[0]
        text = text.split(', indirizzo')[0]
    if model == CLAUDE_3_5_HAIKU:
        # TODO: Possibly make a function for the post-processing below.
        text = text.split(": ")[0]
        text = text.split(" - ")[0]
        # e.g. design, per unire la mia creatività con competenze tecniche moderne
        # e.g. scienze della comunicazione, perché mi affascina il mondo dei media e della comunicazione digitale
        text = text.split(", per")[0]
        # [INFO] Doing Model claude_3_5_haiku | Language it | Temperature 0.3 | Prompt type llm_as_student | Prompt params file with_names.
        # e.g.: psicologia all'università di bologna, comunicazione e media all'università cattolica di milano
        text = text.split(" all'università ")[0]
        text = text.split(" al politecnico ")[0]
        text = text.split(" presso l'università")[0]
        text = text.split(" con indirizzo")[0]
        text = text.strip()
    # Perform the mapping of different wordings.
    if language == IT:
        if text in COURSE_MAPPINGS_IT:  # TODO I have to add the check on the language
            text = COURSE_MAPPINGS_IT[text]
    return text


def parse_with_multiple_patterns(text, patterns):
    # NB: the order of the patterns is relevant!!
    for pattern in patterns:
        match = re.findall(pattern, text)
        if match:
            return match
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
