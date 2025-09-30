from pydantic import BaseModel


class BaseConfig(BaseModel):
    class Config:
        validate_by_name = True


class ExchangeRate(BaseConfig):
    course: float
