from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    neo4j_uri: str = "bolt://127.0.0.1:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "password"

    llm_provider: str = "openai"
    llm_model: str = "openai/gpt-4o-mini"
    openai_api_key: str = ""
    openai_base_url: str = "https://openrouter.ai/api/v1"

    host: str = "0.0.0.0"
    port: int = 8001
    
    api_key: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
