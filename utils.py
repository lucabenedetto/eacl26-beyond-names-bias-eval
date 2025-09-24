from utils_anthropic import get_anthropic_response
from utils_google import get_google_response
from utils_open_ai import get_openai_response
from constants import (
    OPENAI_MODEL_TO_API_NAME,
    ANTHROPIC_MODEL_TO_API_NAME,
    GOOGLE_MODEL_TO_API_NAME,
    NAMES_F, NAMES_M, ADJECTIVES_M, ADJECTIVES_F, ADJECTIVES_X, NOUNS_M, NOUNS_F, NOUNS_X,
)
from langchain_core.prompts import ChatPromptTemplate
from langchain_aws import ChatBedrockConverse


def get_llm_response(api_key, model, prompt, temperature):
    if model in OPENAI_MODEL_TO_API_NAME:
        try:
            response = get_openai_response(
                api_key=api_key,
                system_context='',
                user_prompt=prompt,
                model=OPENAI_MODEL_TO_API_NAME[model],
                temperature=temperature,
            )
        except Exception as e:
            print(e)
            response = "{'index': -9, 'text': 'None'}"  # this if the GPT model did not produce a response
    elif model in ANTHROPIC_MODEL_TO_API_NAME:
        try:
            llm = ChatBedrockConverse(
                model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
                region_name="us-west-2",
                max_tokens=1000,
                temperature=temperature,
            )

            prompt_for_chain = ChatPromptTemplate.from_messages(
                [
                    ("human", "{input}"),
                ]
            )

            chain = prompt_for_chain | llm

            response = chain.invoke(
                {
                    "input": prompt,
                }
            ).content

        except Exception as e:
            print(e)
            response = "{'index': -9, 'text': 'None'}"  # this if the model did not produce a response
    elif model in GOOGLE_MODEL_TO_API_NAME:
        try:
            response = get_google_response(
                api_key=api_key,
                system_context=None,  # empty string breaks the google API.
                user_prompt=prompt,
                model=GOOGLE_MODEL_TO_API_NAME[model],
                temperature=temperature,
            )
        except Exception as e:
            print(e)
            response = "{'index': -9, 'text': 'None'}"  # this if the model did not produce a response
    else:
        raise ValueError(f"Model {model} not found")
    return response


def get_target_dict_from_df_row(row) -> str:
    # Note that this does not distinguish between different adjectives and nouns in each group (e.g, groups together
    # all adjective in ADJECTIVES_X).
    if not (row['with_name'] or row['with_noun'] or row['with_adjective']):
        return 'model'
    if row['with_name']:  # TODO: This does not work for parsing the rows with names if the adjective/noun is X instead of F/M
        if row['name'] in NAMES_F[row['language']]:
            return 'f'
        if row['name'] in NAMES_M[row['language']]:
            return 'm'
    if row['with_noun']:
        if row['noun'] in NOUNS_F[row['language']]:
            return 'f'
        if row['noun'] in NOUNS_M[row['language']]:
            return 'm'
        if row['noun'] in NOUNS_X[row['language']]:
            return 'x'
    if row['with_adjective']:
        if row['adjective'] in ADJECTIVES_F[row['language']]:
            return 'f'
        if row['adjective'] in ADJECTIVES_M[row['language']]:
            return 'm'
        if row['adjective'] in ADJECTIVES_X[row['language']]:
            return 'x'
    raise ValueError(f"Error with row ({row}).")


def to_be_skipped_due_to_empty_recommendation(row):
    # TODO: possibly re-make with a loop.
    return (row.ssd_rec_0 == "NONE" or row.ssd_rec_1 == "NONE" or row.ssd_rec_2 == "NONE"
            or row.ssd_rec_3 == "NONE" or row.ssd_rec_4 == "NONE")
