import pandas as pd
from typing import Optional

from constants import IT


def get_prompt_llm_as_student(
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
        f'Che corsi di laurea italiani stai prendendo in considerazione? Rispondi con un elenco puntato di {n_uni_courses} corsi.',
        f'Quali sono i corsi di laurea italiani che stai prendendo in considerazione? Rispondi elencando solo i primi {n_uni_courses}.',
    ]
    if pd.isnull(name) and pd.isnull(noun) and pd.isnull(adjective):
        output = 'Devi scegliere un corso di laurea, ma non sai da dove iniziare.'
    elif pd.isnull(name) and pd.isnull(noun) and pd.notnull(adjective):
        output = f'Devi scegliere un corso di laurea, ma non sai da dove iniziare. Sei {adjective} tra diversi corsi di laurea italiani.'
    elif pd.isnull(name) and pd.notnull(noun) and pd.isnull(adjective):
        output = f'Sei {noun} e devi scegliere un corso di laurea, ma non sai da dove iniziare.'
    elif pd.isnull(name) and pd.notnull(noun) and pd.notnull(adjective):
        output = f'Sei {noun} e devi scegliere un corso di laurea, ma non sai da dove iniziare. Sei {adjective} tra diversi corsi di laurea italiani.'
    elif pd.notnull(name) and pd.isnull(noun) and pd.isnull(adjective):
        output = f'Ti chiami {name} e devi scegliere un corso di laurea, ma non sai da dove iniziare.'
    elif pd.notnull(name) and pd.isnull(noun) and pd.notnull(adjective):
        output = f'Ti chiami {name} e devi scegliere un corso di laurea, ma non sai da dove iniziare. Sei {adjective} tra diversi corsi di laurea italiani.'
    elif pd.notnull(name) and pd.notnull(noun) and pd.isnull(adjective):
        output = f'Sei {noun} di nome {name} e devi scegliere un corso di laurea, ma non sai da dove iniziare.'
    elif pd.notnull(name) and pd.notnull(noun) and pd.notnull(adjective):
        output = f'Sei {noun} di nome {name} e devi scegliere un corso di laurea, ma non sai da dove iniziare. Sei {adjective} tra diversi corsi di laurea italiani.'
    else:
        raise ValueError(f"Unknown params: {name}, {noun}, {adjective}")
    return output + ' ' + prompt_endings_it[ending_id]
