from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    mongodb_url: str
    mongodb_db: str

    dummyjson_api_base_url: str
    dummyjson_timeout: int = 10

    api_title: str = "Leads API"
    api_version: str = "1.0.0"
    api_description: str = "API para gerenciamento de Leads"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_",
        case_sensitive=False
    )

settings = Settings()