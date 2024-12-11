import pandas as pd
from constants import (
    NAMES_F_IT, 
    NAMES_M_IT,
    IT,
)

ADJECTIVES_M = {
    IT: {'indeciso'},
}
ADJECTIVES_F = {
    IT: {'indecisa'},
}
ADJECTIVES_N = {
    IT: {'indecisə', 'indecis*'},
}
NOUNS_M = {
    IT: {'uno studente'},
}
NOUNS_F = {
    IT: {'una studentessa'},
}
NOUNS_N = {
    IT: {'unə studentə', 'un* student*'},
}


def prepare_new_row_df(row, name):
    return pd.DataFrame({
        'language': [row.language],
        'with_name': [True],
        'with_noun': [row.with_noun],
        'with_adjective': [row.with_adjective],
        'name': [name],
        'noun': [row.noun],
        'adjective': [row.adjective],
        'n_uni_courses': [row.n_uni_courses],
        'ending_id': [row.ending_id],
    })


def main(language: str):
    # TODO: dosctring with all params
    # This method creates, starting from a .csv file with the experimental parameters *without* student names, the
    # files with the parameters for the experiments with names. These parameters are then used to create the prompts
    # used for the experiments.
    # the params_no_name_{language}.csv file which is used as a starting point has to be manually curated (it is already
    # available in this repo, as well as the params_with_names* files, meaning that you don't have to re-run this script
    # to reproduce the results shown in the paper but can directly re-use those param files.
    df = pd.read_csv(f'params_no_name_{language}.csv')
    out_df = pd.DataFrame(columns=df.columns)

    for row in df.itertuples():
        if (not row.with_noun and not row.with_adjective) or row.adjective in ADJECTIVES_N[language]  or row.noun in NOUNS_N[language]:
            for name in NAMES_F_IT + NAMES_M_IT:
                if len(out_df) == 0:
                    out_df = prepare_new_row_df(row, name).copy()
                else:
                    out_df = pd.concat([out_df, prepare_new_row_df(row, name)], ignore_index=True)
        elif row.adjective in ADJECTIVES_F[IT]  or row.noun in NOUNS_F[IT]:
            for name in NAMES_F_IT:
                out_df = pd.concat([out_df, prepare_new_row_df(row, name)], ignore_index=True)
        elif row.adjective in ADJECTIVES_M[IT] or row.noun in NOUNS_M[IT]:
            for name in NAMES_M_IT:
                out_df = pd.concat([out_df, prepare_new_row_df(row, name)], ignore_index=True)
    out_df.to_csv(f'params_with_names_{language}.csv', index=False)

    out_df = pd.DataFrame(columns=df.columns)
    for row in df.itertuples():
        for name in NAMES_F_IT + NAMES_M_IT:
            new_row_df = prepare_new_row_df(row, name)
            if len(out_df) == 0:
                out_df = new_row_df.copy()
            else:
                out_df = pd.concat([out_df, new_row_df], ignore_index=True)
    out_df.to_csv(f'params_with_names_all_combinations_{language}.csv', index=False)


if __name__ == '__main__':
    LANGUAGE = IT
    main(LANGUAGE)
