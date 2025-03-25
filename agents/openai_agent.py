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

    def generate_content(self, context: str, prompt: str) -> str:
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
                        "text": context,
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