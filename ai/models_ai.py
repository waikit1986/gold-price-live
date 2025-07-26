from sqlalchemy import Column, String, Float, Integer, Date
from db.database import Base

class AiAnalysisBase(Base):
    __abstract__ = True

    date = Column(Date, primary_key=True)
    symbol = Column(String, primary_key=True)
    directional_bias = Column(String)
    key_drivers = Column(String)
    macro_alignment = Column(String)
    risk_signals = Column(String)
    today_outlook = Column(String)
    today_entry_price = Column(Float)
    today_target_price = Column(Float)
    today_stop_loss = Column(Float)
    today_confidence_level = Column(String)
    today_confidence_score = Column(Integer)
    today_confirmation_trigger = Column(String)
    today_invalidation_level = Column(String)
    today_trade_signal = Column(String)
    short_term_outlook = Column(String)
    short_term_entry_price = Column(Float)
    short_term_target_price = Column(Float)
    short_term_stop_loss = Column(Float)
    short_term_confidence_level = Column(String)
    short_term_confidence_score = Column(Integer)
    short_term_confirmation_trigger = Column(String)
    short_term_invalidation_level = Column(String)
    short_term_trade_signal = Column(String)
    summary = Column(String)
    detail_summary = Column(String)

class AiAnalysis1D(AiAnalysisBase):
    __tablename__ = "ai_analysis_1d"

class AiAnalysis1H(AiAnalysisBase):
    __tablename__ = "ai_analysis_1h"
