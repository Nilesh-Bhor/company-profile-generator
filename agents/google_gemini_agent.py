import os
from google import genai
from google.genai import types
from agents.base_agent import BaseAgent
# from models.models import CompanyProfileResponse

class GoogleGeminiAgent(BaseAgent):
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        super().__init__(model_name)
        GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
        self.client = genai.Client(api_key=GOOGLE_API_KEY)

    def generate_content(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
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

        # response_text = response.text.strip()
        # profile_response = self.validate_response(response_text)
        # return profile_response