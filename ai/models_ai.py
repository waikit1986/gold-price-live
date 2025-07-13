from sqlalchemy import Column, String, Float, Integer, Date
from db.database import Base

class AiAnalysis(Base):
    __tablename__ = "ai_analysis"

    date = Column(Date, primary_key=True)
    symbol = Column(String, primary_key=True)
    directional_bias = Column(String)
    key_drivers = Column(String)
    macro_alignment = Column(String)
    risk_signals = Column(String)
    short_term_outlook = Column(String)
    entry_price = Column(Float)
    target_price = Column(Float)
    stop_loss = Column(Float)
    confidence_level = Column(String)
    confidence_score = Column(Integer)
    confirmation_trigger = Column(String)
    invalidation_level = Column(String)
    trade_signal = Column(String)
