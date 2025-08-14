import os
from pydantic_settings import BaseSettings
import logging
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    ANTHROPIC_BASE_URL: str = os.getenv("ANTHROPIC_BASE_URL", "your_default_url")
    # Only one of ANTHROPIC_API_KEY or ANTHROPIC_AUTH_TOKEN is required
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "your_default_key")
    ANTHROPIC_AUTH_TOKEN: str = os.getenv("ANTHROPIC_AUTH_TOKEN", "your_default_token")
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "your_default_model")

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "sk-REPLACE_ME") # set your own API key here
    LOG_LEVEL: str = "INFO"

    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    RELOAD: bool = bool(os.getenv("RELOAD", True))

settings = Settings()
logger.info(f"Settings loaded: {settings}")
