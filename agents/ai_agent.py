from enum import Enum
from core.settings import Settings
from agents.base_agent import BaseAgent
from agents.openai_agent import OpenAIAgent
from agents.google_gemini_agent import GoogleGeminiAgent

class AgentType(Enum):
    GOOGLE_GEMINI = "google_gemini"
    OPENAI = "openai"

class AIAgent:
    @staticmethod
    def get_agent(agent_type: AgentType) -> BaseAgent:
        if agent_type == AgentType.GOOGLE_GEMINI:
            return GoogleGeminiAgent()
        elif agent_type == AgentType.OPENAI:
            model_name = 'gpt-4o-mini'
            use_perplexity = Settings.USE_PERPLEXITY
            if use_perplexity:
                model_name = 'sonar'

            return OpenAIAgent(model_name=model_name, use_perplexity=Settings.USE_PERPLEXITY)
            
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")