"""
Class to handle imports from .env file and keep it in Setting class object
"""
from pydantic_settings import BaseSettings, SettingsConfigDict

class Setting(BaseSettings):
    """
    Class to handle import from .env file
    """
    BOT_API_KEY: str
    STOCK_KEY_API: str
    STOCK_API_URL: str
    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env")
