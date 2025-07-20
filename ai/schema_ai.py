from pydantic import BaseModel
from datetime import date


class AiResponseBase(BaseModel):
    directional_bias: str
    key_drivers: str
    macro_alignment: str
    risk_signals: str
    short_term_outlook: str
    entry_price: float
    target_price: float
    stop_loss: float
    confidence_level: str
    confidence_score: int
    confirmation_trigger: str
    invalidation_level: str
    trade_signal: str
    summary: str
    detail_summary: str

    class Config:
        from_attributes = True


class AiResponse(AiResponseBase):
    pass


class AiResponseToSave(AiResponseBase):
    date: date
