from pydantic import BaseModel
import datetime


class AiResponse(BaseModel):
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
   
   class Config():
     from_attributes = True
   
class AiResponseToSave(BaseModel):
   date: datetime.date
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