from typing import Optional
from transformers import AutoTokenizer, AutoModelForCausalLM

from src.base_llm_recommender import BaseLLMRecommender
from constants import (
    HUGGINGFACE_MODEL_NAMES,
)

class HuggingFaceLLMRecommender(BaseLLMRecommender):

    def __init__(self,
                 model_name: str,
                 access_token: str = None,
                 use_gpu: bool = False,
                 ) -> None:
        super().__init__(model_name)
        self.use_gpu = use_gpu
        self.tokenizer = AutoTokenizer.from_pretrained(HUGGINGFACE_MODEL_NAMES[model_name], token=access_token)
        if self.use_gpu:
            self.model = AutoModelForCausalLM.from_pretrained(HUGGINGFACE_MODEL_NAMES[model_name], token=access_token, device_map="auto")
        else:
            self.model = AutoModelForCausalLM.from_pretrained(HUGGINGFACE_MODEL_NAMES[model_name], token=access_token)

    def perform_recommendation(self,
                               user_prompt: str,
                               temperature: float,
                               system_message: Optional[str] = None,
                               **kwargs
                               ) -> str:
        input_text = self.prepare_input_text(user_prompt)
        input_ids = self.tokenizer(input_text, return_tensors="pt")
        if self.use_gpu:
            input_ids = input_ids.to('cuda')
        outputs = self.model.generate(
            **input_ids,
            max_new_tokens=1000,    # TODO make the max_new_tokens a param
            pad_token_id=self.tokenizer.eos_token_id,
        )  # TODO: add temperature.
        start_index = len(input_text)  # TODO: I have to check this!
        response = self.tokenizer.decode(outputs[0])[start_index:]
        return response

    # TODO
    def prepare_input_text(self, user_prompt: str, system_message: Optional[str] = None) -> str:
        raise NotImplementedError()
        # input_text = self.prompt
        # if self.model_name == LLAMA_3_8B:
        #     input_text = "<|begin_of_text|>\n<|start_header_id|>system<|end_header_id|>\n" + input_text + "<|eot_id|>\n<|start_header_id|>user<|end_header_id|>"
        # if self.model_name == MISTRAL_7B_v02:
        #     input_text = "<s>[INST] " + input_text
        # input_text += f"Text: '{text}'\n\n"
        # if self.model_name == LLAMA_3_8B:
        #     input_text = input_text + "\n<|eot_id|>\n<|start_header_id|>assistant<|end_header_id|>\n"
        # if self.model_name == MISTRAL_7B_v02:
        #     input_text = input_text + " [/INST]"
        # return input_text
