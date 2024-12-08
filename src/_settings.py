from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGODB_HOST: str = "localhost"
    MONGODB_PORT: int = 27017
    MONGODB_USER: str = ""
    MONGODB_PASSWORD: str = ""
    MONGODB_NAME: str = ""

    MYSQL_HOST: str = "localhost"
    MYSQL_USER: str = ""
    MYSQL_PASSWORD: str = ""
    MYSQL_NAME: str = ""

    GPT_MODEL: str = "gpt-4o"
    OPENAI_API_KEY: str = ""


settings = Settings(_env_file=".env")

if __name__ == "__main__":
    print(settings)
