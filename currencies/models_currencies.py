from db.database import Base
from sqlalchemy import Column, DateTime, Float


class Xau(Base):
    __tablename__ = 'xau'
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    price = Column(Float)
    # bid = Column(Float)
    # ask = Column(Float)

class LbmaXauAm(Base):
    __tablename__ = 'lbma_xau_am'
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    price = Column(Float)

class LbmaXauPm(Base):
    __tablename__ = 'lbma_xau_pm'
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    price = Column(Float)

class Xag(Base):
    __tablename__ = 'xag'
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    price = Column(Float)
    # bid = Column(Float)
    # ask = Column(Float)

class LbmaXag(Base):
    __tablename__ = 'lbma_xag'
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    price = Column(Float)

class Xpt(Base):
    __tablename__ = 'xpt'
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    price = Column(Float)
    # bid = Column(Float)
    # ask = Column(Float)

class LbmaXptAm(Base):
    __tablename__ = 'lbma_xpt_am'
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    price = Column(Float)

class LbmaXptPm(Base):
    __tablename__ = 'lbma_xpt_pm'
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    price = Column(Float)

class Xpd(Base):
    __tablename__ = 'xpd'
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    price = Column(Float)
    # bid = Column(Float)
    # ask = Column(Float)

class LbmaXpdAm(Base):
    __tablename__ = 'lbma_xpd_am'
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    price = Column(Float)

class LbmaXpdPm(Base):
    __tablename__ = 'lbma_xpd_pm'
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    price = Column(Float)
    
class BrentCrude(Base):
    __tablename__ = 'brent_crude'
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    price = Column(Float)
    
class EUR(Base):
    __tablename__ = 'eur'
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    price = Column(Float)
    
class JPY(Base):
    __tablename__ = 'jpy'
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    price = Column(Float)
    
class CNY(Base):
    __tablename__ = 'cny'
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    price = Column(Float)