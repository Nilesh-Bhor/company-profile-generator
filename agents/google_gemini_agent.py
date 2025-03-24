import os
from google import genai
from google.genai import types
from agents.base_agent import BaseAgent

class GoogleGeminiAgent(BaseAgent):
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        super().__init__(model_name)
        self.initialize_client()
    
    def initialize_client(self):
        GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
        self.client = genai.Client(api_key=GOOGLE_API_KEY)

    def generate_content(self, prompt: str) -> str:
        optimized_prompt = f"""
            {prompt}
            
            ### CONTEXT ###
            We want to dynamically create a company profile with all needed information.
            **Yahoo Finance**, Crunchbase, S&P Capital IQ, and other financial databases are good sources for financial information.
            Company websites, press releases, and news articles are good sources for general information.
            Local newspapers, government websites, and industry-specific websites are good sources for local information.
             ***IMPORTANT - Please ensure all data is accurate, up-to-date, and include sources.*** \n

            Please provide a response in a structured JSON format that matches the following schema: {self.schema}'
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