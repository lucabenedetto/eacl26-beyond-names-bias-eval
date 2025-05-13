import ast

import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

data_path = "./data/processed_output/stem_magnitude_ssd_coordinates_recs.csv"  # changed this myself

df = pd.read_csv(data_path)
models_recs = dict()

for model, model_df in df.groupby('model'):
    if model not in models_recs:
        models_recs[model] = dict()
    for prompt_type, prompt_df in model_df.groupby('prompt_type'):
        if prompt_type not in models_recs[model]:
            models_recs[model][prompt_type] = dict()
        for study_group, study_group_df in prompt_df.groupby('study_group'):
            if study_group not in models_recs[model][prompt_type]:
                models_recs[model][prompt_type][study_group] = dict()
            for recs in study_group_df['recommendations'].tolist():  # changed this myself
                recs = ast.literal_eval(recs)
                for i, rec in enumerate(recs):
                    if rec not in models_recs[model][prompt_type][study_group]:
                        models_recs[model][prompt_type][study_group][rec] = 0
                    models_recs[model][prompt_type][study_group][rec] += (5 - i)

df_list = []
for model in models_recs:
    for prompt_type in models_recs[model]:
        for study_group in models_recs[model][prompt_type]:
            sorted_recs = dict(
                sorted(models_recs[model][prompt_type][study_group].items(), key=lambda item: item[1], reverse=True))
            temp_df = pd.DataFrame(list(sorted_recs.items()), columns=['Recommendation', 'Score'])
            temp_df['Model'] = model
            temp_df['Prompt Type'] = prompt_type
            temp_df['Study Group'] = study_group
            df_list.append(temp_df)
df = pd.concat(df_list)
model_family_dict = {"claude_3_5_haiku": 'claude', "claude_3_5_sonnet": 'claude', "gemini_1_5": 'gemini',
                     "gemini_1_5_8b": 'gemini', "gpt_3_5": 'gpt', "gpt_4o": 'gpt', "gpt_4o_mini": 'gpt'}
df['Model Family'] = df['Model'].replace(model_family_dict)

for prompt_type, prompt_df in df.groupby("Prompt Type"):
    for current_model, current_model_df in prompt_df.groupby("Model"):
        print(current_model_df)
        current_model_df['Normalized Score'] = current_model_df.groupby("Study Group")["Score"].transform(
            lambda x: x / x.sum())
        top_recs = current_model_df.groupby("Recommendation")["Normalized Score"].mean().sort_values(ascending=False)[:7]
        current_model_df = current_model_df[current_model_df['Recommendation'].isin(top_recs.index)]
        fig = plt.figure(figsize=(16, 9))
        fig.suptitle(f"Model: {current_model}, Prompt Type: {prompt_type}")
        ax = fig.add_subplot(1, 1, 1)
        sns.barplot(current_model_df, x="Normalized Score", y="Recommendation", hue="Study Group", order=top_recs.index,
                    orient="y")
        plt.tight_layout()
        # plt.show()
        plt.savefig(
            f"./figures/2025_05_08_for_paper/{current_model}_{prompt_type}.png")  # changed this myself
