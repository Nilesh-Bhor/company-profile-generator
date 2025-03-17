from enum import Enum
from agents.openai_agent import OpenAIAgent
from agents.google_gemini_agent import GoogleGeminiAgent

class AgentType(Enum):
    GOOGLE_GEMINI = "google_gemini"
    OPENAI = "openai"

class AgentFactory:
    @staticmethod
    def get_agent(agent_type: AgentType):
        if agent_type == AgentType.GOOGLE_GEMINI:
            return GoogleGeminiAgent()
        elif agent_type == AgentType.OPENAI:
            return OpenAIAgent()
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")