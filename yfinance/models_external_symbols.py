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

class GLD(Base, BasePrice): __tablename__ = "gld_1d"
class GCF(Base, BasePrice): __tablename__ = "gc_1d"
class IAU(Base, BasePrice): __tablename__ = "iau_1d"
class SIF(Base, BasePrice): __tablename__ = "si_f_1d"
class PPLT(Base, BasePrice): __tablename__ = "pplt_1d"
class PALL(Base, BasePrice): __tablename__ = "pall_1d"
class DXY(Base, BasePrice): __tablename__ = "dxy_1d"
class TNX(Base, BasePrice): __tablename__ = "tnx_1d"
class TIP(Base, BasePrice): __tablename__ = "tip_1d"
class CLF(Base, BasePrice): __tablename__ = "cl_f_1d"
class VIX(Base, BasePrice): __tablename__ = "vix_1d"
class GSPC(Base, BasePrice): __tablename__ = "gspc_1d"
