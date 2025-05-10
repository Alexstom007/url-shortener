from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    HOST: str = '127.0.0.1'
    PORT: int = 8080
    API_PREFIX: str = '/api/v1'
    API_TITLE: str = 'URL Service'
    API_VERSION: str = '1.0.0'
    BASE_URL: str = f'http://{HOST}:{PORT}'

    class Config:
        env_file = '.env'
        case_sensitive = True


settings = Settings()
