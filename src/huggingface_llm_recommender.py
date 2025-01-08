# import torch
from typing import Optional, List, Dict
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import pipeline
from src.base_llm_recommender import BaseLLMRecommender
from constants import (
    HUGGINGFACE_MODEL_NAMES,
    LLAMA_3_8B,
)

class HuggingFaceLLMRecommender(BaseLLMRecommender):

    def __init__(self,
                 model_name: str,
                 access_token: str = None,
                 # use_gpu: bool = False,
                 ) -> None:
        super().__init__(model_name)
        self.pipe = pipeline(
            task="text-generation",
            model=HUGGINGFACE_MODEL_NAMES[model_name],
            device_map="auto",
            token=access_token,
        )
        # The code below was used for an older version of transformers
        #   (for transformers >= 4.43.0 I can use the pipeline as above).
        # self.use_gpu = use_gpu
        # self.tokenizer = AutoTokenizer.from_pretrained(HUGGINGFACE_MODEL_NAMES[model_name], token=access_token)
        # if self.use_gpu:
        #     self.model = AutoModelForCausalLM.from_pretrained(HUGGINGFACE_MODEL_NAMES[model_name], token=access_token, device_map="auto")
        # else:
        #     self.model = AutoModelForCausalLM.from_pretrained(HUGGINGFACE_MODEL_NAMES[model_name], token=access_token)

    def perform_recommendation(self,
                               user_prompt: str,
                               temperature: float,
                               system_message: Optional[str] = None,
                               **kwargs
                               ) -> str:
        if system_message is None:
            system_message = ""
        messages = [{"role": "system", "content": system_message}, {"role": "user", "content": user_prompt}]
        outputs = self.pipe(
            messages,
            max_new_tokens=512, # TODO make the max_new_tokens a param
            temperature=temperature,
            do_sample=True,
        )
        response = outputs[0]["generated_text"][-1]["content"]
        # print("RESPONSE:")
        # print(response)
        # print("END RESPONSE:")
        return response
        # The code below was used for an older version of transformers
        #   (for transformers >= 4.43.0 I can use the pipeline as above).
        # input_text = self.prepare_complete_prompt(user_prompt)
        # input_ids = self.tokenizer(input_text, return_tensors="pt")
        # if self.use_gpu:
        #     input_ids = input_ids.to('cuda')
        # outputs = self.model.generate(
        #     **input_ids,
        #     max_new_tokens=1000,    # TODO make the max_new_tokens a param
        #     pad_token_id=self.tokenizer.eos_token_id,
        # )  # TODO: add temperature.
        # start_index = len(input_text)  # TODO: I have to check this!
        # response = self.tokenizer.decode(outputs[0])[start_index:]
        # return response

    # The code below was needed for an older version of transformers
    #   (for transformers >= 4.43.0 I can use the pipeline as above).
    # def prepare_complete_prompt(self, user_prompt: str, system_message: Optional[str] = None) -> str:
    #     if system_message is None:
    #         system_message = ""
    #     complete_prompt = system_message
    #     if self.model_name in {LLAMA_3_8B}:
    #         complete_prompt = "<|begin_of_text|>\n<|start_header_id|>system<|end_header_id|>\n" + system_message + "<|eot_id|>\n<|start_header_id|>user<|end_header_id|>"
    #     complete_prompt += f"{user_prompt}\n"
    #     if self.model_name in {LLAMA_3_8B}:
    #         complete_prompt = complete_prompt + "\n<|eot_id|>\n<|start_header_id|>assistant<|end_header_id|>\n"
    #     return complete_prompt

    def perform_recommendation_whole_dataset(self,
                                             user_prompts: List[str],
                                             temperature: float,
                                             system_message: Optional[str] = None,
                                             **kwargs
                                             ) -> List[str]:
        if system_message is None:
            system_message = ""

        # Prepare dataset from prompts
        prompts = [{"user_prompt": prompt, "system_message": system_message} for prompt in user_prompts]
        dataset = Dataset.from_list(prompts)

        # Map the pipeline to the dataset
        def generate_response(batch):
            messages = [
                {"role": "system", "content": batch.get("system_message", "")},
                {"role": "user", "content": batch["user_prompt"]}
            ]
            outputs = self.pipe(
                messages,
                max_new_tokens=512,  # TODO make the max_new_tokens a param
                temperature=temperature,
                do_sample=True,
            )
            return {"response": outputs[0]["generated_text"][-1]["content"]}

        # Apply the pipeline in batch
        dataset = dataset.map(generate_response, batched=False)
        return dataset["response"]
        #
        # messages = [{"role": "system", "content": system_message}, {"role": "user", "content": user_prompt}]
        # outputs = self.pipe(
        #     messages,
        #     max_new_tokens=512, # TODO make the max_new_tokens a param
        #     temperature=temperature,
        #     do_sample=True,
        # )
        # response = outputs[0]["generated_text"][-1]["content"]
        # # print("RESPONSE:")
        # # print(response)
        # # print("END RESPONSE:")
        # return response
