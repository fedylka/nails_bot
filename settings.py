from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMINS: list[int] 

    class Config:
        env_file = ".env"

settings = Settings()