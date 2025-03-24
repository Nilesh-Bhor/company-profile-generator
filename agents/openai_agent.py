import os
import json
from openai import OpenAI
from agents.base_agent import BaseAgent

class OpenAIAgent(BaseAgent):
    def __init__(self, model_name: str = "gpt-4o-mini"):
        super().__init__(model_name)
        self.initialize_client()

    def initialize_client(self):
        OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def generate_content(self, prompt: str) -> str:
        messages = [
            {
                "role": "system", 
                "content": "You are a helpful assistant."
            },
            {
                "role": "user", 
                "content": [
                    {
                        "type": "text",
                        "text": (
                            """
                            ### CONTEXT ###
                            We aim to dynamically generate a comprehensive company profile with accurate, up-to-date information. The data should be sourced from reliable financial databases, official company communications, and credible industry sources to ensure accuracy and credibility.
                            """
                            """
                            ### **Primary Data Sources:**  
                            - **Financial Information:** Yahoo Finance, Crunchbase, S&P Capital IQ, Bloomberg, annual reports, and investor relations websites.  
                            - **General Company Information:** Official company websites, press releases, news articles, and corporate filings.  
                            - **Geographic and Local Data:** Government websites, local newspapers, industry-specific websites, and regulatory filings.  
                            """
                            """
                            ### **Critical Requirements:**  
                            - Ensure **accuracy and cross-verification** of financial data.  
                            - Provide **source attribution** for key figures and statements.  
                            - Use **latest available data** (e.g., last 5 fiscal years for financials).  
                            - Include **key strategic initiatives and major corporate events** from the past 3-5 years.  
                            - Cover **market position, competitive landscape, and client base** where relevant.  
                            """
                        ),
                    },
                    {
                        "type": "text",
                        "text": prompt,
                    }
                ]
            }
        ]
    
        # Call the OpenAI ChatCompletion API
        response = self.client.chat.completions.create(
            model = self.model_name,
            messages = messages,
            top_p = 1,
            presence_penalty = 0,
            frequency_penalty = 0,
            temperature = 0,
            response_format = {
                "type": "json_schema",
                "json_schema": json.loads(self.schema),
            }
        )
        
        # Extract the summary from the response
        summary = response.choices[0].message.content.strip()
        return summary