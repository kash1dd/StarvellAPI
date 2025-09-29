from pydantic import BaseModel, Field

class BaseConfig(BaseModel):
    class Config:
        validate_by_name = True

class TelegramStarvellSettings(BaseModel):
    id: int
    username: str | None

class Settings(BaseModel):
    email_notifications_enabled: bool = Field(alias="emailNotificationsEnabled")
    telegram_notifications_enabled: bool = Field(alias="telegramNotificationsEnabled")
    is_offers_visible_only: bool = Field(alias="isOffersVisibleOnlyInProfile")

class PreviewSettings(BaseModel):
    starvell_settings: Settings = Field(alias="settings")
    telegram_settings: TelegramStarvellSettings | None = Field(alias="telegramLink")