from pydantic_settings import BaseSettings, SettingsConfigDict

from pydantic import (
    Field,
    BaseModel,
    PostgresDsn,
    RedisDsn,
    MongoDsn,
    KafkaDsn,
)




class PostgresSettings(BaseModel):
    user: str = "admin"
    password: str
    host: str = "postgres"
    port: int = 5432
    db: str = "db"
    schema_: str = "public"

    # Connection pool
    pool_size: int = 10
    max_overflow: int = 20
    pool_recycle: int = 3600

    dsn: PostgresDsn = ...


class RedisSettings(BaseModel):
    host: str = "redis"
    port: int = 6379
    db: int = 0
    password: str | None = None

    dsn: RedisDsn = ...



class MongoSettings(BaseModel):
    host: str = "mongo"
    port: int = 27017
    user: str = "admin"
    password: str
    db: str = "db"

    dsn: MongoDsn = ...



class KafkaSettings(BaseModel):
    dsn: KafkaDsn = ...


class JWTSettings(BaseModel):
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",  # В .env можно писать POSTGRES__USER=admin , приставки берутся по названию полей в Settings
        case_sensitive=False,
        extra="ignore",
    )

    # FastAPI server 
    host: str = "0.0.0.0"
    port: int = 8080

    # Other services
    postgres: PostgresSettings = PostgresSettings()
    redis: RedisSettings = RedisSettings()
    mongo: MongoSettings = MongoSettings()
    kafka: KafkaSettings = KafkaSettings()
    jwt: JWTSettings = JWTSettings()


settings = Settings()