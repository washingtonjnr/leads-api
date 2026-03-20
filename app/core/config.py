from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    mongodb_url: str
    mongodb_db: str

    dummyjson_api_base_url: str
    dummyjson_timeout: int = 10

    api_title: str = "Leads API"
    api_version: str = "1.0.0"
    api_description: str = "API para gerenciamento de Leads"

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_expire_minutes: int = 30
    jwt_refresh_expire_days: int = 1

    jira_url: str
    jira_email: str
    jira_api_token: str
    jira_webhook_secret: str = ""
    jira_timeout: int = 10

    ai_provider: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_",
        case_sensitive=False,
        extra="ignore"
    )

settings = Settings()