from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    token_ttl: int = 20
    SECRET_KEY: str = 'a21679097c1ba42e9bd06eea239cdc5bf19b249e87698625cba5e3572f005544'
    ALGORITHM: str = 'HS256'

settings = Settings()