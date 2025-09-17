"""
This is the same as 04_2_pca_reduction_ssd_coordinates.py but using t-SNE instead of PCA for dimensionality reduction.
"""
import numpy as np
import os
import pandas as pd
import pickle
from sklearn.manifold import TSNE

from constants import (
    MODELS_BY_OWNER,
    C_MODEL, C_STUDY_GROUP, C_TEMPERATURE, C_RECS, C_LANGUAGE, C_PROMPT_TYPE, C_PROMPT_PARAM, C_TSNE_0, C_TSNE_1,
    C_LIST_SSD,
)


def tsne_reduction(
        coordinates,
        perplexity: int = 50,
        learning_rate: int = 200,
        random_state: int = 42,
):
    # TODO test with other params, and make them tunable by changing the functions parameters.
    model = TSNE(n_components=2, perplexity=perplexity, learning_rate=learning_rate, random_state=random_state)
    transformed_coordinates = model.fit_transform(np.array(coordinates))
    return model, transformed_coordinates


# TODO: move this, it is a duplicate of the one in 04_2_pca_reduction_ssd_coordinates.py
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

    # Train t-SNE on the all dataset and perform the conversion.
    coordinates = convert_df_to_coordinates(df)
    # TODO: tests with other params
    print("[INFO] Ready to fit t-SNE model aggregate.")
    tsne_model, transformed_full_list = tsne_reduction(coordinates, perplexity=50, learning_rate=200, random_state=42)
    # Store the t-SNE reduced list
    out_df = df.copy()
    out_df[C_TSNE_0] = transformed_full_list[:, 0]
    out_df[C_TSNE_1] = transformed_full_list[:, 1]
    out_df = out_df[[C_MODEL, C_LANGUAGE, C_PROMPT_TYPE, C_PROMPT_PARAM, C_TEMPERATURE, C_STUDY_GROUP, C_TSNE_0, C_TSNE_1, C_RECS]]
    out_df.to_csv(os.path.join('data', 'processed_output', 'tsne_reduced_ssd_coordinates_aggregate.csv'), index=False)
    with open("data/processed_output/tsne_model_aggregate.pkl", "wb") as file:
        pickle.dump(tsne_model, file)

    # Then, perform t-SNE separately for each "family" of models.
    for model_owner, models in MODELS_BY_OWNER.items():
        local_df = df[df[C_MODEL].isin(models)]
        coordinates = convert_df_to_coordinates(local_df)
        # TODO: tests with other params
        print("[INFO] Ready to fit t-SNE model %s." % model_owner)
        tsne_model, transformed_full_list = tsne_reduction(coordinates, perplexity=50, learning_rate=200, random_state=42)
        out_df = local_df.copy()
        out_df[C_TSNE_0] = transformed_full_list[:, 0]
        out_df[C_TSNE_1] = transformed_full_list[:, 1]
        out_df = out_df[[C_MODEL, C_LANGUAGE, C_PROMPT_TYPE, C_PROMPT_PARAM, C_TEMPERATURE, C_STUDY_GROUP, C_TSNE_0, C_TSNE_1, C_RECS]]
        out_df.to_csv(os.path.join('data', 'processed_output', f'tsne_reduced_ssd_coordinates_{model_owner}.csv'), index=False)
        with open(f"data/processed_output/tsne_model_{model_owner}.pkl", "wb") as file:
            pickle.dump(tsne_model, file)


if __name__ == '__main__':
    main()
