from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str="Autonomous Multi-Agent Intelligence System"
    environment: str="development"
    notify_threshold: int=70
    openai_api_key: str=""
    openai_model: str="gpt-5-mini"
    model_config=SettingsConfigDict(env_file=".env",extra="ignore")

settings=Settings()
