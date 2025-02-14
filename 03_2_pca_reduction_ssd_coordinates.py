"""
This script uses thestem_magnitude_ssd_coordinates_recs.csv file produced by the
`04_1_compute_stem_magnitude_and_ssd_coordinates.py` script.
It performs PCA on the whole dataset and stores the PCA reduced coordinates in a new file.
It also performs PCA separately for each "family" of models (grouping them by owner), and stored the PCA reduced
coordinates in a new file for each of those.
It is meant to be run after the `04_1_compute_stem_magnitude_and_ssd_coordinates.py` script, and to be run once on all
the models and prompt types.
"""
import numpy as np
import os
import pandas as pd
import pickle
from sklearn.decomposition import PCA

from constants import (
    MODELS_BY_OWNER,
    C_MODEL, C_STUDY_GROUP, C_TEMPERATURE, C_RECS, C_LANGUAGE, C_PROMPT_TYPE, C_PROMPT_PARAM, C_PCA_0, C_PCA_1,
    C_LIST_SSD,
)


def pca_reduction(coordinates):
    pca = PCA(n_components=2)
    transformed_full_list = pca.fit_transform(coordinates)
    return pca, transformed_full_list


def convert_df_to_coordinates(df):
    coordinates_list = list()
    for index, (_, row) in enumerate(df.iterrows()):
        coordinates = np.zeros(14)
        for idx in range(14):
            coordinates[idx] = row[C_LIST_SSD[idx]]
        coordinates_list.append(coordinates)
    return coordinates_list

def main():
    df = pd.read_csv(os.path.join('data', 'processed_output', 'stem_magnitude_ssd_coordinates_recs.csv'))

    # Train PCA on the whole dataset and perform the conversion.
    coordinates = convert_df_to_coordinates(df)
    pca, transformed_full_list = pca_reduction(coordinates)
    # Store the PCA reduced list
    out_df = df.copy()
    out_df[C_PCA_0] = transformed_full_list[:, 0]
    out_df[C_PCA_1] = transformed_full_list[:, 1]
    out_df = out_df[[C_MODEL, C_LANGUAGE, C_PROMPT_TYPE, C_PROMPT_PARAM, C_TEMPERATURE, C_STUDY_GROUP, C_PCA_0, C_PCA_1, C_RECS]]
    out_df.to_csv(os.path.join('data', 'processed_output', 'pca_reduced_ssd_coordinates_aggregate.csv'), index=False)
    with open("data/processed_output/pca_model_aggregate.pkl", "wb") as file:
        pickle.dump(pca, file)

    # Then, perform PCA separately for each "family" of models.
    for model_owner, models in MODELS_BY_OWNER.items():
        local_df = df[df[C_MODEL].isin(models)]
        coordinates = convert_df_to_coordinates(local_df)
        pca, transformed_full_list = pca_reduction(coordinates)
        out_df = local_df.copy()
        out_df[C_PCA_0] = transformed_full_list[:, 0]
        out_df[C_PCA_1] = transformed_full_list[:, 1]
        out_df = out_df[[C_MODEL, C_LANGUAGE, C_PROMPT_TYPE, C_PROMPT_PARAM, C_TEMPERATURE, C_STUDY_GROUP, C_PCA_0, C_PCA_1, C_RECS]]
        out_df.to_csv(os.path.join('data', 'processed_output', f'pca_reduced_ssd_coordinates_{model_owner}.csv'), index=False)
        with open(f"data/processed_output/pca_model_{model_owner}.pkl", "wb") as file:
            pickle.dump(pca, file)


if __name__ == '__main__':
    main()
