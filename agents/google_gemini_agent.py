import os
from google import genai
from google.genai import types
from agents.base_agent import BaseAgent

class GoogleGeminiAgent(BaseAgent):
    def __init__(self):
        GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
        self.client = genai.Client(api_key=GOOGLE_API_KEY)

    def generate_content(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model="gemini-2.0-flash", 
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