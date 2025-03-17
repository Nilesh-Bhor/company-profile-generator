import os
from openai import OpenAI, models
from agents.base_agent import BaseAgent

class OpenAIAgent(BaseAgent):
    def __init__(self):
        OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def generate_content(self, prompt: str) -> str:
        response = self.client.responses.create(
            model="gpt-4o",
            instructions="You are an expert research analyst.",
            input=prompt,
        )
        return response.output_text