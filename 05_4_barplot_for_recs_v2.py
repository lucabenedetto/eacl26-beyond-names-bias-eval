import ast

import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from constants import (
    C_STUDY_GROUP,
)
from course_mappings import LIST_SSD


# TODO: Possibly move these to the constants or course mappings file.
LIST_SSD_IDS = ['SSD_0','SSD_1','SSD_2','SSD_3','SSD_4','SSD_5','SSD_6','SSD_7','SSD_8','SSD_9','SSD_10','SSD_11','SSD_12','SSD_13']
MAP_SSD_ID_TO_NAME = {ssd: LIST_SSD[idx] for idx, ssd in enumerate(LIST_SSD_IDS)}
print(MAP_SSD_ID_TO_NAME)

data_path = "./data/processed_output/stem_magnitude_ssd_coordinates_recs.csv"  # changed this myself
df = pd.read_csv(data_path)

# Here you can add the filter on model / prompt type / etc.
df_recommended_ssd_count = df.groupby(C_STUDY_GROUP).sum()[LIST_SSD_IDS]
# this DF has one row for each study group, and one column for each SSD. The value of each cell is the frequency of the recommendation of the corresponding SSD (normalised)
df_normalized = df_recommended_ssd_count.div(df_recommended_ssd_count.sum(axis=1), axis=0).reset_index()
print(df_normalized)

# pd.melt is turning wide-format data into long-format
df_melted = pd.melt(df_normalized, id_vars=['study_group'], var_name='SSD', value_name='Score')
# print(df_melted)
df_melted['ssd_name'] = df_melted.apply(lambda r: MAP_SSD_ID_TO_NAME[r['SSD']], axis=1)
print(df_melted)

# This is to get the list of most frequently recommended SSD
top_recs = df_melted.groupby("ssd_name")["Score"].mean().sort_values(ascending=False)[:5]
df_melted = df_melted[df_melted['ssd_name'].isin(top_recs.index)]

current_model = 'aggregate'
prompt_type = 'aggregate'

# Here is the code for the plot.
fig = plt.figure(figsize=(16, 9))
fig.suptitle(f"Model: {current_model}, Prompt Type: {prompt_type}")
ax = fig.add_subplot(1, 1, 1)
sns.barplot(df_melted, x="Score", y="ssd_name", hue="study_group", order=top_recs.index, orient="y")
plt.tight_layout()
plt.show()
