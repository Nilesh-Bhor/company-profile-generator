import os
from openai import OpenAI
from agents.base_agent import BaseAgent
# from models.models import CompanyProfileResponse

class OpenAIAgent(BaseAgent):
    def __init__(self, model_name: str = "gpt-4o-mini"):
        super().__init__(model_name)
        OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def generate_content(self, prompt: str) -> str:
        response = self.client.responses.create(
            model=self.model_name,
            instructions="You are an expert research analyst.",
            input=prompt,
        )
        return response.output_text.strip()

        # response_text = response.output_text.strip()
        # profile_response = self.validate_response(response_text)
        # return profile_response