import pandas as pd
from typing import Optional

from constants import IT


def get_prompt_user_as_student(
        language,
        name: Optional[str] = None,
        noun: Optional[str] = None,  # un{a/o/ə/*} student{e/essa/ə/*}
        adjective: Optional[str] = None,  # indecis{a/o/ə/*}
        n_uni_courses: int = 5,
        ending_id: int = 0,
):
    if language == IT:
        return get_prompt_it(name, noun, adjective, n_uni_courses, ending_id)
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
