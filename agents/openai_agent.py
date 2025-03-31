import json
from openai import OpenAI
from core.settings import Settings
from agents.base_agent import BaseAgent


class OpenAIAgent(BaseAgent):
    def __init__(self, model_name: str = "gpt-4o-mini", use_perplexity: bool = False):
        super().__init__(model_name)
        self.use_perplexity = use_perplexity

    def generate_content(self, context: str, prompt: str) -> str:
        client = None
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{context}\n\n{prompt}"}
        ]
        
        if self.use_perplexity:
            client = OpenAI(api_key=Settings.PERPLEXITY_API_KEY, base_url=Settings.PERPLEXITY_BASE_URL)
        else:
            client = OpenAI(api_key=Settings.OPENAI_API_KEY)

        response = client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=0,
            response_format={
                "type": "json_schema",
                "json_schema": { "schema": json.loads(self.schema) },
            }
        )

        # Extract the summary from the response
        summary = response.choices[0].message.content.strip()
        return summary
