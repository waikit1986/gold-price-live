from sqlalchemy import Column, Float, Date
from sqlalchemy import BigInteger 

from db.database import Base

class BasePrice:
    date = Column(Date, primary_key=True, index=True)
    price = Column(Float)
    close = Column(Float)
    high = Column(Float)
    low = Column(Float)
    open = Column(Float)
    volume = Column(BigInteger)


class GLD(Base, BasePrice): __tablename__ = "gld"
class GCF(Base, BasePrice): __tablename__ = "gc"
class IAU(Base, BasePrice): __tablename__ = "iau"
class SIF(Base, BasePrice): __tablename__ = "si_f"
class PPLT(Base, BasePrice): __tablename__ = "pplt"
class PALL(Base, BasePrice): __tablename__ = "pall"
class DXY(Base, BasePrice): __tablename__ = "dxy"
class TNX(Base, BasePrice): __tablename__ = "tnx"
class TIP(Base, BasePrice): __tablename__ = "tip"
class CLF(Base, BasePrice): __tablename__ = "cl_f"
class VIX(Base, BasePrice): __tablename__ = "vix"
class GSPC(Base, BasePrice): __tablename__ = "gspc"
