from sqlalchemy import Column, DateTime, Float, String
from db.database import Base

class IndicatorFeatureBase(Base):
    __abstract__ = True
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    price = Column(Float)
    indicator = Column(String, primary_key=True)
    value = Column(Float)

class IndicatorFeatureXau(IndicatorFeatureBase):
    __tablename__ = "xau_indicators"

class IndicatorFeatureXag(IndicatorFeatureBase):
    __tablename__ = "xag_indicators"

class IndicatorFeatureXpt(IndicatorFeatureBase):
    __tablename__ = "xpt_indicators"

class IndicatorFeatureXpd(IndicatorFeatureBase):
    __tablename__ = "xpd_indicators"

class IndicatorFeatureBrentCrude(IndicatorFeatureBase):
    __tablename__ = "brent_crude_indicators"

class IndicatorFeatureEur(IndicatorFeatureBase):
    __tablename__ = "eur_indicators"

class IndicatorFeatureJpy(IndicatorFeatureBase):
    __tablename__ = "jpy_indicators"

class IndicatorFeatureCny(IndicatorFeatureBase):
    __tablename__ = "cny_indicators"
