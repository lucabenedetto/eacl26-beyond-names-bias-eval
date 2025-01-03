from typing import Optional

class BaseLLMRecommender(object):

    def __init__(self, model_name: str):
        self.model_name = model_name

    def perform_recommendation(self,
                               user_prompt: str,
                               temperature: float,
                               system_message: Optional[str] = None,
                               **kwargs
                               ) -> str:
        raise NotImplementedError("perform_recommendation not implemented for the Base class, use the other classes.")

    def prepare_input_text(self, user_prompt: str, system_message: Optional[str]) -> str:
        raise NotImplementedError("prepare_input_text not implemented for the Base class, use the other classes.")
