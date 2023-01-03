from pydantic import BaseSettings


class CommonSettings(BaseSettings):
    APP_NAME: str = "FastAPI GraphQL Starter"
    DEBUG_MODEL: bool = False


class ServerSettings(BaseSettings):
    HOST: str = "127.0.0.1"
    PORT: int = 8000


class DatabaseSettings(BaseSettings):
    DB_URL: str = ''
    DB_NAME: str = ''


class InfrastructureSettings(BaseSettings):
    AWS_ACCOUNT: str = ""
    AWS_REGION: str = ""
    ENV_TYPE: str = "dev"
    DOMAIN_NAME: str = ""


class Settings(CommonSettings, DatabaseSettings, ServerSettings,
               InfrastructureSettings):
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()

