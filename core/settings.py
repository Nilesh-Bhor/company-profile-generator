import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    FMP_API_KEY = os.getenv("FMP_API_KEY", "")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY", "")
    PERPLEXITY_BASE_URL = "https://api.perplexity.ai"
    AGENT_TYPE = os.getenv("AGENT_TYPE", "GOOGLE_GEMINI")
    WKHTMLTOPDF_PATH = os.getenv("WKHTMLTOPDF_PATH", "")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "")
    USE_PERPLEXITY =  os.getenv('USE_PERPLEXITY', 'False').lower() == 'true'

settings = Settings()