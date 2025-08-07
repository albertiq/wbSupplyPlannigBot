from pydantic import ConfigDict, Field, PostgresDsn, computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    wb_token: str = Field("", alias="WB_TOKEN")
    bot_token: str = Field("", alias="BOT_TOKEN")

    postgres_user: str = Field("wb_planner", alias="PG_USER")
    postgres_password: str = Field(..., alias="PG_PASSWORD")
    postgres_host: str = Field(default="localhost", alias="PG_HOST")
    postgres_port: int = Field(default=5432, alias="PG_PORT")
    postgres_database: str = Field(default="supply_planning", alias="PG_DATABASE")

    analytics_api_url: str = Field("https://seller-analytics-api.wildberries.ru/api")
    supplies_api_url: str = Field("https://supplies-api.wildberries.ru/api")

    support_username: str = Field("user", alias="SUPPORT_USERNAME")
    timezone: str = Field("Asia/Yekaterinburg", alias="TZ")

    @computed_field
    @property
    def postgres_dsn(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            path=self.postgres_database,
        )


cfg = Settings()
