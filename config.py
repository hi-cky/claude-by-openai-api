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
logger.info(" === Configuration Loaded ===")
logger.info(f" Host: {settings.HOST}:{settings.PORT}")
logger.info(f" Default Model: {settings.DEFAULT_MODEL}")
logger.info(f" Log Level: {settings.LOG_LEVEL}")
logger.info(f" Reload: {settings.RELOAD}")
logger.info(f" ANTHROPIC_BASE_URL: {settings.ANTHROPIC_BASE_URL}")
logger.info(f" ANTHROPIC_API_KEY: {settings.ANTHROPIC_API_KEY}")
logger.info(f" ANTHROPIC_AUTH_TOKEN: {settings.ANTHROPIC_AUTH_TOKEN}")
logger.info(f" OPENAI_API_KEY: {settings.OPENAI_API_KEY}")
