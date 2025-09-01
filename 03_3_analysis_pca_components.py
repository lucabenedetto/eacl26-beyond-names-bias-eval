"""
This short script shows the components of the PCA model, both printing them at screen (with the name of the corresponding 
s.s.d.), and plotting them as a bar plot.
"""
import numpy as np
import pickle
import matplotlib.pyplot as plt

from constants import MODELS_BY_OWNER
from course_mappings import LIST_SSD, MAP_SSD_TO_STEM, LIST_SSD_EN

plt.rcParams.update({
    "font.size": 16,
    "font.family": "serif",
})


def plot_pca_components(model_owner, output_filename=None):
    pca_model = pickle.load(open(f'data/processed_output/pca_model_{model_owner}.pkl', 'rb'))

    fig, ax = plt.subplots(figsize=(16, 8))
    bar_width = 0.4
    y_positions = np.arange(len(LIST_SSD))
    hatch = ['//' if MAP_SSD_TO_STEM.get('%02d' % (i+1), False) else '' for i in range(len(LIST_SSD))]  # bars with forward slashes are STEM disciplines.
    ax.barh(y_positions - bar_width / 2, pca_model.components_[0], height=bar_width, label="PCA 0", hatch=hatch)
    ax.barh(y_positions + bar_width / 2, pca_model.components_[1], height=bar_width, label="PCA 1", hatch=hatch)
    ax.set_yticks(y_positions)
    # ax.set_yticklabels([x if len(x) < 20 else x[:18]+'...' for x in LIST_SSD])
    ax.set_yticklabels([LIST_SSD_EN[idx] for idx in range(len(LIST_SSD))])
    # ax.set_xlabel("Values")
    # ax.set_title(f"Components of the trained PCA model")
    ax.legend()
    ax.grid(axis='both')
    fig.tight_layout()
    if output_filename is None:
        plt.show()
    else:
        plt.savefig(output_filename)
        plt.close()


def plot_pca_explained_variance(model_owner, output_filename=None):
    pca_model = pickle.load(open(f'data/processed_output/pca_model_{model_owner}.pkl', 'rb'))

    explained_variance_ratio = pca_model.explained_variance_ratio_

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(range(1, len(explained_variance_ratio) + 1), explained_variance_ratio, alpha=0.7, align='center')
    ax.step(range(1, len(explained_variance_ratio) + 1), explained_variance_ratio.cumsum(), where='mid', linestyle='--', color='red')  # the cumulative sum
    ax.set_xlabel('Principal Component Index')
    ax.set_ylabel('Explained Variance Ratio')
    ax.set_title('Explained Variance by Principal Components')
    ax.set_xticks(range(1, len(explained_variance_ratio) + 1))
    ax.grid(True)
    fig.tight_layout()
    if output_filename is None:
        plt.show()
    else:
        plt.savefig(output_filename)
        plt.close()


if __name__ == '__main__':
    RUN_DATE = '2025_05_for_paper'

    plot_pca_components(model_owner='aggregate', output_filename=f'figures/{RUN_DATE}/pca_components_aggregate.png')
    plot_pca_explained_variance(model_owner='aggregate', output_filename=f'figures/{RUN_DATE}/pca_explained_variance_aggregate.png')
    # for model_owner in MODELS_BY_OWNER.keys():
    #     plot_pca_components(model_owner=model_owner, output_filename=f'figures/{RUN_DATE}/pca_components_{model_owner}.png')
    #     plot_pca_explained_variance(model_owner=model_owner, output_filename=f'figures/{RUN_DATE}/pca_explained_variance_{model_owner}.png')
