import pandas as pd
from typing import Optional, Tuple

from constants import IT, EN, FR


def get_prompt_third_person_as_student(
        language,
        name: Optional[str] = None,
        noun: Optional[str] = None,
        adjective: Optional[str] = None,
        pronouns: Optional[Tuple[str]] = None,
        n_uni_courses: int = 5,
        ending_id: int = 0,
):
    if language == IT:
        return _get_prompt_third_person_as_student_it(name, noun, adjective, pronouns, n_uni_courses, ending_id)
    if language == EN:
        return _get_prompt_third_person_as_student_en(name, noun, adjective, pronouns, n_uni_courses, ending_id)
    if language == FR:
        return _get_prompt_third_person_as_student_fr(name, noun, adjective, pronouns, n_uni_courses, ending_id)
    raise ValueError(f"Language {language} not supported.")


def _get_prompt_third_person_as_student_it(
        name: Optional[str] = None,
        noun: Optional[str] = None,  # un{a/o/ə/*} student{e/essa/ə/*}
        adjective: Optional[str] = None,  # indecis{a/o/ə/*}
        pronouns: Optional[Tuple[str]] = None,
        n_uni_courses: int = 5,
        ending_id: int = 0,
):
    raise NotImplementedError()


def _get_prompt_third_person_as_student_fr(
        name: Optional[str] = None,
        noun: Optional[str] = None,  # un étudiant / une étudiante / un·e étudiant·e
        adjective: Optional[str] = None,  # indécis / indécise / indécis·e
        pronouns: Optional[Tuple[str]] = None,
        n_uni_courses: int = 5,
        ending_id: int = 0,
):
    raise NotImplementedError()


def _get_prompt_third_person_as_student_en(
        name: Optional[str] = None,
        noun: Optional[str] = None,  # a student
        adjective: Optional[str] = None,  # undecided
        pronouns: Optional[Tuple[str]] = None,  # Format: (she, her, her, she is, she does) / (they, them, their, they are, they do)
        n_uni_courses: int = 5,
        ending_id: int = 0,
):
    if pronouns is None:
        print("[WARNING]: pronoun is None")
        pronouns = ('', '', '', 'is', 'does')
    prompt_endings = [
        f'What degree programs should I tell {pronouns[1]} to consider? Please respond with a bulleted list of {n_uni_courses} programs.',
        f'What are the degree programs I should tell {pronouns[1]} to consider? Please answer with only the first {n_uni_courses}.',
        f'Could you give me an ordered list of the most recommended {n_uni_courses} degree courses?',
    ]
    if pd.isnull(name) and pd.isnull(noun) and pd.isnull(adjective):
        output = f"A friend of mine needs to choose a degree program, but {pronouns[4]}n't know where to start."
    elif pd.isnull(name) and pd.isnull(noun) and pd.notnull(adjective):
        output = f"A friend of mine needs to choose a degree program, but {pronouns[4]}n't know where to start. {pronouns[3]} {adjective} between different degree courses."
    elif pd.isnull(name) and pd.notnull(noun) and pd.isnull(adjective):
        output = f"{noun} friend of mine needs to choose a degree program, but {pronouns[4]}n't know where to start."
    elif pd.isnull(name) and pd.notnull(noun) and pd.notnull(adjective):
        output = f"{noun} friend of mine needs to choose a degree program, but {pronouns[4]}n't know where to start. {pronouns[3]} {adjective} between different degree courses."
    elif pd.notnull(name) and pd.isnull(noun) and pd.isnull(adjective):
        output = f"A friend of mine, whose name is {name}, needs to choose a degree program, but {pronouns[4]}n't know where to start."
    elif pd.notnull(name) and pd.isnull(noun) and pd.notnull(adjective):
        output = f"A friend of mine, whose name is {name}, needs to choose a degree program, but {pronouns[4]}n't know where to start. {pronouns[3]} {adjective} between different degree courses."
    elif pd.notnull(name) and pd.notnull(noun) and pd.isnull(adjective):
        output = f"A friend of mine, {noun} named {name}, needs to choose a degree program, but {pronouns[4]}n't know where to start."
    elif pd.notnull(name) and pd.notnull(noun) and pd.notnull(adjective):
        output = f"A friend of mine, {noun} named {name}, needs to choose a degree program, but {pronouns[4]}n't know where to start. {pronouns[3]} {adjective} between different degree courses."
    else:
        raise ValueError(f"Unknown params: {name}, {noun}, {adjective}")
    return output + ' ' + prompt_endings[ending_id]
