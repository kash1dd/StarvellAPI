from pydantic import BaseModel

class ExchangeRate(BaseModel):
    course: float