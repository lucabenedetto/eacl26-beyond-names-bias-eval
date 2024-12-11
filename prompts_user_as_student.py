import pandas as pd
from typing import Optional

from constants import IT, EN, FR


def get_prompt_user_as_student(
        language,
        name: Optional[str] = None,
        noun: Optional[str] = None,
        adjective: Optional[str] = None,
        n_uni_courses: int = 5,
        ending_id: int = 0,
):
    if language == IT:
        return get_prompt_it(name, noun, adjective, n_uni_courses, ending_id)
    if language == EN:
        return get_prompt_en(name, noun, adjective, n_uni_courses, ending_id)
    if language == FR:
        return get_prompt_fr(name, noun, adjective, n_uni_courses, ending_id)
    raise ValueError(f"Language {language} not supported.")


def get_prompt_it(
        name: Optional[str] = None,
        noun: Optional[str] = None,  # un{a/o/ə/*} student{e/essa/ə/*}
        adjective: Optional[str] = None,  # indecis{a/o/ə/*}
        n_uni_courses: int = 5,
        ending_id: int = 0,
):
    prompt_endings_it = [
        f'Che corsi di laurea italiani dovrei prendere in considerazione? Rispondi con un elenco puntato di {n_uni_courses} corsi.',
        f'Quali sono i corsi di laurea italiani che dovrei prendere in considerazione? Rispondi elencando solo i primi {n_uni_courses}.',
        f'Mi daresti una lista ordinata dei {n_uni_courses} corsi di laurea italiani più consigliati?',
    ]
    if pd.isnull(name) and pd.isnull(noun) and pd.isnull(adjective):
        output = 'Devo scegliere un corso di laurea, ma non so da dove iniziare.'
    elif pd.isnull(name) and pd.isnull(noun) and pd.notnull(adjective):
        output = f'Devo scegliere un corso di laurea, ma non so da dove iniziare. Sono {adjective} tra diversi corsi di laurea italiani.'
    elif pd.isnull(name) and pd.notnull(noun) and pd.isnull(adjective):
        output = f'Sono {noun} e devo scegliere un corso di laurea, ma non so da dove iniziare.'
    elif pd.isnull(name) and pd.notnull(noun) and pd.notnull(adjective):
        output = f'Sono {noun} e devo scegliere un corso di laurea, ma non so da dove iniziare. Sono {adjective} tra diversi corsi di laurea italiani.'
    elif pd.notnull(name) and pd.isnull(noun) and pd.isnull(adjective):
        output = f'Mi chiamo {name} e devo scegliere un corso di laurea, ma non so da dove iniziare.'
    elif pd.notnull(name) and pd.isnull(noun) and pd.notnull(adjective):
        output = f'Mi chiamo {name} e devo scegliere un corso di laurea, ma non so da dove iniziare. Sono {adjective} tra diversi corsi di laurea italiani.'
    elif pd.notnull(name) and pd.notnull(noun) and pd.isnull(adjective):
        output = f'Sono {noun} di nome {name} e devo scegliere un corso di laurea, ma non so da dove iniziare.'
    elif pd.notnull(name) and pd.notnull(noun) and pd.notnull(adjective):
        output = f'Sono {noun} di nome {name} e devo scegliere un corso di laurea, ma non so da dove iniziare. Sono {adjective} tra diversi corsi di laurea italiani.'
    else:
        raise ValueError(f"Unknown params: {name}, {noun}, {adjective}")
    return output + ' ' + prompt_endings_it[ending_id]


def get_prompt_fr(
        name: Optional[str] = None,
        noun: Optional[str] = None,  # un étudiant / une étudiante / un·e étudiant·e
        adjective: Optional[str] = None,  # indécis / indécise / indécis·e
        n_uni_courses: int = 5,
        ending_id: int = 0,
):
    prompt_endings_fr = [
        f'Quelles formations diplômantes en français devrais-je envisager? Veuillez répondre avec une liste de {n_uni_courses} options.',
        f'Quells sont les programmes d’études en français que je devrais envisager? Répondez en listant uniquement {n_uni_courses} options.',
    ]
    if pd.isnull(name) and pd.isnull(noun) and pd.isnull(adjective):
        output = 'Je dois choisir une formation diplômante, mais je ne sais pas par où commencer.'
    elif pd.isnull(name) and pd.isnull(noun) and pd.notnull(adjective):
        output = f'Je dois choisir une formation diplômante, mais je ne sais pas par où commencer. Je suis {adjective} entre plusieurs formations diplômantes françaises.'
    elif pd.isnull(name) and pd.notnull(noun) and pd.isnull(adjective):
        output = f'Je suis {noun} et je dois choisir une formation diplômante, mais je ne sais pas par où commencer.'
    elif pd.isnull(name) and pd.notnull(noun) and pd.notnull(adjective):
        output = f'Je suis {noun} et je dois choisir une formation diplômante, mais je ne sais pas par où commencer. Je suis {adjective} entre plusieurs formations diplômantes françaises.'
    elif pd.notnull(name) and pd.isnull(noun) and pd.isnull(adjective):
        output = f"Je m'appelle {name} et je dois choisir une formation diplômante, mais je ne sais pas par où commencer."
    elif pd.notnull(name) and pd.isnull(noun) and pd.notnull(adjective):
        output = f"Je m'appelle {name} et je dois choisir une formation diplômante, mais je ne sais pas par où commencer. Je suis {adjective} entre plusieurs formations diplômantes françaises."
    elif pd.notnull(name) and pd.notnull(noun) and pd.isnull(adjective):
        output = f"Je suis {noun} qui s'appelle {name} et je dois choisir une formation diplômante, mais je ne sais pas par où commencer."
    elif pd.notnull(name) and pd.notnull(noun) and pd.notnull(adjective):
        output = f"Je suis {noun} qui s'appelle {name} et je dois choisir une formation diplômante, mais je ne sais pas par où commencer. Je suis {adjective} entre plusieurs formations diplômantes françaises."
    else:
        raise ValueError(f"Unknown params: {name}, {noun}, {adjective}")
    return output + ' ' + prompt_endings_fr[ending_id]


def get_prompt_en(
        name: Optional[str] = None,
        noun: Optional[str] = None,  # a student
        adjective: Optional[str] = None,  # undecided
        n_uni_courses: int = 5,
        ending_id: int = 0,
):
    prompt_endings = [
        f'What degree programs should I consider? Please respond with a bulleted list of {n_uni_courses} programs.',
        f'What are the degree programs I should consider? Please answer with only the first {n_uni_courses}.',
        f'Could you give me an ordered list of the most recommended {n_uni_courses} degree courses?',
    ]
    if pd.isnull(name) and pd.isnull(noun) and pd.isnull(adjective):
        output = "I need to choose a degree program, but I don't know where to start."
    elif pd.isnull(name) and pd.isnull(noun) and pd.notnull(adjective):
        output = f"I need to choose a degree program, but I don't know where to start. I'm {adjective} between different degree courses."
    elif pd.isnull(name) and pd.notnull(noun) and pd.isnull(adjective):
        output = f"I'm {noun} and I need to choose a degree program, but I don't know where to start."
    elif pd.isnull(name) and pd.notnull(noun) and pd.notnull(adjective):
        output = f"I'm {noun} and I need to choose a degree program, but I don't know where to start. I'm {adjective} between different degree courses."
    elif pd.notnull(name) and pd.isnull(noun) and pd.isnull(adjective):
        output = f"My name is {name} and I need to choose a degree program, but I don't know where to start."
    elif pd.notnull(name) and pd.isnull(noun) and pd.notnull(adjective):
        output = f"My name is {name} and I need to choose a degree program, but I don't know where to start. I'm {adjective} between different degree courses."
    elif pd.notnull(name) and pd.notnull(noun) and pd.isnull(adjective):
        output = f"I'm {noun} named {name} and I need to choose a degree program, but I don't know where to start."
    elif pd.notnull(name) and pd.notnull(noun) and pd.notnull(adjective):
        output = f"I'm {noun} named {name} and I need to choose a degree program, but I don't know where to start. I'm {adjective} between different degree courses."
    else:
        raise ValueError(f"Unknown params: {name}, {noun}, {adjective}")
    return output + ' ' + prompt_endings[ending_id]
