from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    wb_token: str = Field("", alias="WB_TOKEN")
    bot_token: str = Field("", alias="BOT_TOKEN")


cfg = Settings()
