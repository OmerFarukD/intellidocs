from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    APP_NAME: str = "IntelliDocs"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str
    DATABASE_URL_DOCKER:str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # OpenAI
    OPENAI_API_KEY: str

    class Config:
        env_file = ".env"

    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8001
# Singleton — her yerden bu objeyi import edersin
settings = Settings()
