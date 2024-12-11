import pandas as pd
from constants import (
    NAMES_F_IT, 
    NAMES_M_IT,
)


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


def main():
    df = pd.read_csv('params_no_name.csv')
    out_df = pd.DataFrame(columns=df.columns)

    for row in df.itertuples():
        if (not row.with_noun and not row.with_adjective) or row.adjective in ('indecisə', 'indecis*')  or row.noun in ('unə studentə', 'un* student**'):
            for name in NAMES_F_IT + NAMES_M_IT:
                new_row_df = prepare_new_row_df(row, name)
                if len(out_df) == 0:
                    out_df = new_row_df.copy()
                else:
                    out_df = pd.concat([out_df, new_row_df], ignore_index=True)
        elif row.adjective == 'indecisa'  or row.noun == 'una studentessa':
            for name in NAMES_F_IT:
                new_row_df = prepare_new_row_df(row, name)
                out_df = pd.concat([out_df, new_row_df], ignore_index=True)
        elif row.adjective == 'indeciso'  or row.noun == 'uno studente':
            for name in NAMES_M_IT:
                new_row_df = prepare_new_row_df(row, name)
                out_df = pd.concat([out_df, new_row_df], ignore_index=True)
    out_df.to_csv('params_with_names.csv', index=False)

    out_df = pd.DataFrame(columns=df.columns)
    for row in df.itertuples():
        for name in NAMES_F_IT + NAMES_M_IT:
            new_row_df = prepare_new_row_df(row, name)
            if len(out_df) == 0:
                out_df = new_row_df.copy()
            else:
                out_df = pd.concat([out_df, new_row_df], ignore_index=True)
    out_df.to_csv('params_with_names_all_combinations.csv', index=False)


if __name__ == '__main__':
    main()
