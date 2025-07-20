from db.database import Base
from sqlalchemy import Column, DateTime, Float


class LbmaXauAm(Base):
    __tablename__ = 'lbma_xau_am_1d'
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    price = Column(Float)

class LbmaXauPm(Base):
    __tablename__ = 'lbma_xau_pm_1d'
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    price = Column(Float)

class LbmaXag(Base):
    __tablename__ = 'lbma_xag_1d'
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    price = Column(Float)

class LbmaXptAm(Base):
    __tablename__ = 'lbma_xpt_am_1d'
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    price = Column(Float)

class LbmaXptPm(Base):
    __tablename__ = 'lbma_xpt_pm_1d'
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    price = Column(Float)

class LbmaXpdAm(Base):
    __tablename__ = 'lbma_xpd_am_1d'
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    price = Column(Float)

class LbmaXpdPm(Base):
    __tablename__ = 'lbma_xpd_pm_1d'
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    price = Column(Float)

class Xau(Base):
    __tablename__ = 'xau_1d'
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    price = Column(Float)
    bid = Column(Float)
    ask = Column(Float)

class Xag(Base):
    __tablename__ = 'xag_1d'
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    price = Column(Float)
    bid = Column(Float)
    ask = Column(Float)

class Xpt(Base):
    __tablename__ = 'xpt_1d'
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    price = Column(Float)
    bid = Column(Float)
    ask = Column(Float)

class Xpd(Base):
    __tablename__ = 'xpd_1d'
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    price = Column(Float)
    bid = Column(Float)
    ask = Column(Float)

class BrentCrude(Base):
    __tablename__ = 'brent_crude_1d'
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    price = Column(Float)

class EUR(Base):
    __tablename__ = 'eur_1d'
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    price = Column(Float)

class JPY(Base):
    __tablename__ = 'jpy_1d'
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    price = Column(Float)

class CNY(Base):
    __tablename__ = 'cny_1d'
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    price = Column(Float)
