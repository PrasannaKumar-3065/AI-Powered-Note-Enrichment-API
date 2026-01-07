from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "dummy"
    OPENAI_API_KEY: str = "dummy"
    OPEN_API_URL: str = "dummy"
    GEMINI_API_KEY: str = "dummy"
    GEMINI_API_URL: str = "dummy"
    MAX_TOKENS: int = 1000

    class Config:
        env_file = ".env"

settings = Settings()