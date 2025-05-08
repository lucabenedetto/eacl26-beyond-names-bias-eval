import itertools
import pathlib

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.preprocessing import RobustScaler

from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from scipy.stats import gaussian_kde


def load_data(filename):
    datapath = pathlib.Path("data/pca")
    df = pd.read_csv(datapath / filename)
    return df


def compute_kde_overlap(cluster1, cluster2, x_min, x_max, y_min, y_max, grid_size):
    """Compute KDE-based overlap by integrating the minimum density function."""
    data1, data2 = np.array(cluster1).T, np.array(cluster2).T
    kde1, kde2 = gaussian_kde(data1), gaussian_kde(data2)

    # Define grid over which to evaluate KDE
    # x_min, x_max = min(data1[0].min(), data2[0].min()), max(data1[0].max(), data2[0].max())
    # y_min, y_max = min(data1[1].min(), data2[1].min()), max(data1[1].max(), data2[1].max())
    x_grid, y_grid = np.linspace(x_min, x_max, grid_size), np.linspace(y_min, y_max, grid_size)
    X, Y = np.meshgrid(x_grid, y_grid)
    positions = np.vstack([X.ravel(), Y.ravel()])

    # Evaluate KDEs on the grid
    density1 = kde1(positions).reshape(grid_size, grid_size)
    density2 = kde2(positions).reshape(grid_size, grid_size)

    # Compute KDE overlap
    kde_overlap = np.sum(np.minimum(density1, density2)) / np.sum(np.maximum(density1, density2))
    return kde_overlap


def get_filtered_df(df, model, prompt_type, temperature):
    print(f"Model: {model}, Prompt Type: {prompt_type}, Temperature: {temperature}")
    if isinstance(model, str):
        model = [model]
    if isinstance(prompt_type, str):
        prompt_type = [prompt_type]
    if isinstance(temperature, float):
        temperature = [temperature]
    filtered_df = df[
        (df.model.isin(model))
        & (df.prompt_type.isin(prompt_type))
        & (df.temperature.isin(temperature))
        ]

    return filtered_df


def compute_kde_overlaps(clusters, labels, x_min, x_max, y_min, y_max, grid_size):
    kde_overlaps = []
    st.write(f"x_min: {x_min}\nx_max: {x_max}\ny_min: {y_min}\ny_max: {y_max}")
    for i in range(4):
        for j in range(4):
            if i == j:
                kde_overlaps.append(
                    {'study_group': labels[i], 'study_group_2': labels[j], 'kde_overlap': np.nan})
            else:
                kde_overlap = compute_kde_overlap(clusters[i], clusters[j], x_min, x_max, y_min, y_max, grid_size)
                kde_overlaps.append({'study_group': labels[i], 'study_group_2': labels[j], 'kde_overlap': kde_overlap})
    kde_overlaps_df = pd.DataFrame(kde_overlaps)
    kde_overlaps_pivot = kde_overlaps_df.pivot(index='study_group', columns='study_group_2', values='kde_overlap')
    return kde_overlaps_pivot


def plot_kde_overlaps(filtered_df, clusters, labels):
    colors = ['blue', 'red', 'green', 'purple']
    # KDE Density Plot
    plt.figure(figsize=(10, 10))
    x_vals = np.linspace(filtered_df['pca_0'].min() - abs(min(0.2 * filtered_df['pca_0'].min(), -1.5)),
                         filtered_df['pca_0'].max() + abs(max(0.2 * filtered_df['pca_0'].max(), 1.5)), 100)
    y_vals = np.linspace(filtered_df['pca_1'].min() - abs(min(0.2 * filtered_df['pca_1'].min(), -1.5)),
                         filtered_df['pca_1'].max() + abs(max(0.2 * filtered_df['pca_1'].max(), 1.5)), 100)
    X, Y = np.meshgrid(x_vals, y_vals)
    for i, cluster in enumerate(clusters):
        kde = gaussian_kde(cluster.T)
        Z = kde(np.vstack([X.ravel(), Y.ravel()])).reshape(X.shape)
        plt.contour(X, Y, Z, colors=colors[i], alpha=0.7)
    legend_handles = [Line2D([0], [0], color=color, lw=2, label=label) for color, label in zip(colors, labels)]
    plt.legend(handles=legend_handles)
    plt.title('KDE Density Contours of 4 Clusters')
    st.pyplot(plt)

st.title("KDE Overlap Visualization")
filenames = ["pca_reduced_ssd_coordinates_aggregate.csv", "pca_reduced_ssd_coordinates_Anthropic.csv", "pca_reduced_ssd_coordinates_Google.csv", "pca_reduced_ssd_coordinates_OpenAI.csv", None]

filename = st.multiselect("Select Filename", filenames, default=None)

if filename:
    dff = load_data(filename[0])
    models = list(dff.model.unique())
    prompt_types = list(dff.prompt_type.unique())
    temperatures = list(dff.temperature.unique())

    selected_models = st.multiselect("Select Models", models, default=models)
    selected_prompt_types = st.multiselect("Select Prompt Types", prompt_types, default=prompt_types)
    selected_temperatures = st.multiselect("Select Temperatures", temperatures, default=temperatures)
    grid_size = st.slider("Grid Size", 10, 1000, 50, 10)
    col_1, col_2 = st.columns(2)
    for c, f, in zip([col_1, col_2], [filename[0], "pca_reduced_ssd_coordinates_aggregate.csv"]):
        with c:
            df = load_data(f)

            filtered_df = get_filtered_df(df, selected_models, selected_prompt_types, selected_temperatures)

            cluster1 = filtered_df[filtered_df.study_group == 'm'][['pca_0', 'pca_1']].values
            cluster2 = filtered_df[filtered_df.study_group == 'f'][['pca_0', 'pca_1']].values
            cluster3 = filtered_df[filtered_df.study_group == 'x'][['pca_0', 'pca_1']].values
            cluster4 = filtered_df[filtered_df.study_group == 'model'][['pca_0', 'pca_1']].values

            x_min = df['pca_0'].min()
            x_max = df['pca_0'].max()
            y_min = df['pca_1'].min()
            y_max = df['pca_1'].max()

            clusters = [cluster1, cluster2, cluster3, cluster4]
            labels = ['m', 'f', 'x', 'model']

            kde_overlaps_df = compute_kde_overlaps(clusters, labels, x_min, x_max, y_min, y_max, grid_size)

            st.write(f"\nKDE-Based Overlaps (file: {f}):")
            st.dataframe(kde_overlaps_df.style.background_gradient(cmap='RdYlGn', axis=1, vmin=0, vmax=1).set_properties(**{'opacity': '0.2'}))

            plot_kde_overlaps(filtered_df, clusters, labels)