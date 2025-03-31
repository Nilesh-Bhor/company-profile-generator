import os
from google import genai
from google.genai import types
from core.settings import Settings
from agents.base_agent import BaseAgent

class GoogleGeminiAgent(BaseAgent):
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        super().__init__(model_name)
        self.initialize_client()
    
    def initialize_client(self):
        self.client = genai.Client(api_key=Settings.GOOGLE_API_KEY)

    def generate_content(self, context: str, prompt: str) -> str:
        optimized_prompt = f"""
            {prompt}
            {context}
        """
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=optimized_prompt,
            config=types.GenerateContentConfig(
                temperature=0,
                tools=[
                    types.Tool(
                        google_search=types.GoogleSearch()
                    )
                ]
            )
        )
        return response.text.strip()