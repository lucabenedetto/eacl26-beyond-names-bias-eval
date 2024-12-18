class BaseLLMRecommender(object):

    def __init__(self, model_name: str):
        self.model_name = model_name

    def perform_recommendation(self, prompt: str, temperature: float, **kwargs) -> str:
        raise NotImplementedError("perform_recommendation not implemented for the Base class, use the other classes.")
