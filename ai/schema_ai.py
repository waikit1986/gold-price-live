from pydantic import BaseModel
from datetime import date

class AiResponseBase(BaseModel):
    directional_bias: str
    key_drivers: str
    macro_alignment: str
    risk_signals: str
    today_outlook: str
    today_entry_price: float
    today_target_price: float
    today_stop_loss: float
    today_confidence_level: str
    today_confidence_score: int
    today_confirmation_trigger: str
    today_invalidation_level: str
    today_trade_signal: str
    short_term_outlook: str
    short_term_entry_price: float
    short_term_target_price: float
    short_term_stop_loss: float
    short_term_confidence_level: str
    short_term_confidence_score: int
    short_term_confirmation_trigger: str
    short_term_invalidation_level: str
    short_term_trade_signal: str
    summary: str
    detail_summary: str

    class Config:
        from_attributes = True


class AiResponse(AiResponseBase):
    pass


class AiResponseToSave(AiResponseBase):
    date: date
    symbol: str
