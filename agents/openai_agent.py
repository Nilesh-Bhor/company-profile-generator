import os
import json
import requests
from openai import OpenAI
from core.settings import Settings
from agents.base_agent import BaseAgent


class OpenAIAgent(BaseAgent):
    def __init__(self, model_name: str = "gpt-4o-mini", use_perplexity: bool = False):
        super().__init__(model_name)
        self.use_perplexity = use_perplexity
    

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
        
        if self.use_perplexity:
            return self.fetch_from_perplexity(messages)
        else:
            return self.fetch_from_openai(messages)

    def fetch_from_openai(self, messages) -> str:
        self.client = OpenAI(api_key=Settings.OPENAI_API_KEY)
    
        # Call the OpenAI ChatCompletion API
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            presence_penalty=0,
            frequency_penalty=0,
            temperature=0,
            response_format={
                "type": "json_schema",
                "json_schema": json.loads(self.schema),
            }
        )
        
        # Extract the summary from the response
        summary = response.choices[0].message.content.strip()
        return summary

    def fetch_from_perplexity(self, messages) -> str:
        url = "https://api.perplexity.ai/v1/query"
        headers = {
            "Authorization": f"Bearer {Settings.PERPLEXITY_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model_name,
            "temperature": 0,
            "stream": False,
            "messages": messages,
            "web_search_options": {"search_context_size": "high"},
            "response_format" : {
                "type": "json_schema",
                "json_schema": json.loads(self.schema),
            }
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            choices = response.json().get("choices")
            message = choices[0].get("message", "")
            return message.get("content").strip()
        else:
            raise Exception(f"Perplexity API Error: {response.status_code} - {response.text}")