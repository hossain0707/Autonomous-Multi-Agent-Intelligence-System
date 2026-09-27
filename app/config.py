from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Autonomous Multi-Agent Intelligence System"
    environment: str = "development"
    notify_threshold: int = 70
    openai_api_key: str = ""
    openai_model: str = "gpt-5-mini"
    github_token: str = ""
    github_repositories: str = ""
    worker_poll_seconds: float = 1.0
    scheduler_enabled: bool = True
    scheduler_tick_seconds: int = 30
    approval_required_for_writes: bool = True
    max_tool_output_chars: int = 12000
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
