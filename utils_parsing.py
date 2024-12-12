from typing import List
from constants import (
    IT, FR, EN,
    GPT_3_5, GPT_4o_MINI,
    CLAUDE_3_5_SONNET, CLAUDE_3_5_HAIKU,
    GEMINI_1_5_FLASH_8B, GEMINI_1_5_FLASH,
    # USER_AS_STUDENT, LLM_AS_STUDENT,
)
import re


def final_cleanup(text: str) -> str:
    # Remove blank spaces at the beginning/end and make everything lowercase.
    text = text.strip().lower()
    # Remove parentheses from the name of the degree.
    if '(' in text and ')' in text:
        text = re.sub(r'\([^()]*\)', ' ', text)
        text = text.strip()
    # Some models do not respond only with the name of the course but also by adding "Degree in..." (in different lang).
    if text[:10] == "laurea in ":
        text = text[10:]
    return text

def parse_with_multiple_patterns(text, patterns):
    # NB: the order of the patterns is relevant!!
    for pattern in patterns:
        match = re.findall(pattern, text)
        if match:
            return [final_cleanup(x) for x in match]
    print("/\\"*20, "\n", text, "/\\"*20, "\n")  # print the text if it didn't match any regex
    return None


def parse_llm_response(response: str, model: str) -> List[str]:
    if model == GPT_3_5:
        return parse_response_gpt_3_5(response)
    if model == GPT_4o_MINI:
        return parse_response_gpt_4o_mini(response)
    if model == GEMINI_1_5_FLASH:
        return parse_response_gemini_1_5_flash(response)
    if model == GEMINI_1_5_FLASH_8B:
        return parse_response_gemini_1_5_flash_8b(response)
    if model == CLAUDE_3_5_HAIKU:
        return parse_response_claude_3_5_haiku(response)
    raise NotImplementedError(f"Model {model} not implemented.")


def parse_response_gpt_3_5(response: str) -> List[str]:
    patterns = [
        r'-\s(.+)',           # Pattern for bullet-point list
        r'\d+\.\s([^\d]+)',   # Pattern for numbered list
    ]
    return parse_with_multiple_patterns(response, patterns)
#     pattern = r'-\s(.+)'
#     # -    --> Matches the literal hyphen at the beginning of each line.
#     # \s   --> Matches the space following the hyphen.
#     # (.+) --> Captures everything after the space until the end of the line (the course name).
#     pattern = r'\d+\.\s([^\d]+)'
#     # \d+ - Matches one or more digits (the numbering of the courses).
#     # \. - Matches the literal period after the number.
#     # \s - Matches the space following the period.
#     # ([^\d]+) - Captures everything that is not a digit (the course name) until the next number is encountered.

def parse_response_gpt_4o_mini(response: str) -> List[str]:
    patterns = [
        r'\*\*(.*?)\*\*',
        r'-\s(.+)',  # Pattern for bullet-point list (same as GPT_3_5)
    ]
    return parse_with_multiple_patterns(response, patterns)
# \*\* - Matches the double asterisks ** that enclose the course name.
# (.*?) - Captures the course name between the double asterisks. The .*? is a non-greedy match to ensure it stops at the closing **.

def parse_response_gemini_1_5_flash(response: str) -> List[str]:
    patterns = [
        r'\*\*(.*?):\*\*', # same as the one for GPT-4o-mini, but with the column (:) between the double asterisks.
        # r'\*\*(.*?):\*\*', # same as the one for GPT-4o-mini, but with the column (:) between the double asterisks.
    ]
    return parse_with_multiple_patterns(response, patterns)

def parse_response_gemini_1_5_flash_8b(response: str) -> List[str]:
    # TODO I have to come back to this one and improve it.
    response = response.replace('\n\n', '\n')
    patterns = [
        r'\*\*(.*?):\*\*', # same as the one for GPT-4o-mini, but with the column (:) between the double asterisks.
        r'\*\s\*\*(.*?)\*\*', # same as the one for GPT-4o-mini, but with the column (:) between the double asterisks.
        # r'\*\s\*\*(.*?):\*\*',
        r'\*\s(.+)',  # Pattern for bullet-point list (almost the same as GPT_3_5, but with asterisk instead of dash)
    ]
    return parse_with_multiple_patterns(response, patterns)


def parse_response_claude_3_5_haiku(response: str) -> List[str]:
    patterns = [
        r'•\s(.+)',  # Pattern for bullet-point list (almost the same as GPT_3_5, but with • instead of dash)
    ]
    match = parse_with_multiple_patterns(response, patterns)
    if match is None:
        return None
    for idx in range(len(match)):
        # TODO: make a function for the post-processing below.
        if ": " in match[idx]:
            match[idx] = match[idx].split(": ")[0]
        if " - " in match[idx]:
            match[idx] = match[idx].split(" - ")[0]
        if ", per" in match[idx]:
            # e.g. design, per unire la mia creatività con competenze tecniche moderne
            # e.g. scienze della comunicazione, perché mi affascina il mondo dei media e della comunicazione digitale
            match[idx] = match[idx].split(", per")[0]
        if " all'università " in match[idx]:
            # [INFO] Doing Model claude_3_5_haiku | Language it | Temperature 0.3 | Prompt type llm_as_student | Prompt params file with_names.
            # e.g.: psicologia all'università di bologna, comunicazione e media all'università cattolica di milano
            match[idx] = match[idx].split(" all'università ")[0]
        if " al politecnico " in match[idx]:
            match[idx] = match[idx].split(" al politecnico ")[0]
    return match
