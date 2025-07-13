from sqlalchemy import Column, Date, DateTime, Float, String
from db.database import Base

class IndicatorFeatureTimeStampBase(Base):
    __abstract__ = True
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    price = Column(Float)
    indicator = Column(String, primary_key=True)
    value = Column(Float)
    
class IndicatorFeatureDateBase(Base):
    __abstract__ = True
    date = Column(Date, primary_key=True)
    price = Column(Float)
    indicator = Column(String, primary_key=True)
    value = Column(Float)

class IndicatorFeatureXau(IndicatorFeatureTimeStampBase):
    __tablename__ = "xau_indicators"

class IndicatorFeatureXag(IndicatorFeatureTimeStampBase):
    __tablename__ = "xag_indicators"

class IndicatorFeatureXpt(IndicatorFeatureTimeStampBase):
    __tablename__ = "xpt_indicators"

class IndicatorFeatureXpd(IndicatorFeatureTimeStampBase):
    __tablename__ = "xpd_indicators"

class IndicatorFeatureBrentCrude(IndicatorFeatureTimeStampBase):
    __tablename__ = "brent_crude_indicators"

class IndicatorFeatureEur(IndicatorFeatureTimeStampBase):
    __tablename__ = "eur_indicators"

class IndicatorFeatureJpy(IndicatorFeatureTimeStampBase):
    __tablename__ = "jpy_indicators"

class IndicatorFeatureCny(IndicatorFeatureTimeStampBase):
    __tablename__ = "cny_indicators"
    
class IndicatorFeatureGLD(IndicatorFeatureDateBase):
    __tablename__ = "gld_indicators"

class IndicatorFeatureGCF(IndicatorFeatureDateBase):
    __tablename__ = "gcf_indicators"

class IndicatorFeatureIAU(IndicatorFeatureDateBase):
    __tablename__ = "iau_indicators"

class IndicatorFeatureSIF(IndicatorFeatureDateBase):
    __tablename__ = "sif_indicators"

class IndicatorFeaturePPLT(IndicatorFeatureDateBase):
    __tablename__ = "pplt_indicators"

class IndicatorFeaturePALL(IndicatorFeatureDateBase):
    __tablename__ = "pall_indicators"

class IndicatorFeatureDXY(IndicatorFeatureDateBase):
    __tablename__ = "dxy_indicators"

class IndicatorFeatureTNX(IndicatorFeatureDateBase):
    __tablename__ = "tnx_indicators"

class IndicatorFeatureTIP(IndicatorFeatureDateBase):
    __tablename__ = "tip_indicators"

class IndicatorFeatureCLF(IndicatorFeatureDateBase):
    __tablename__ = "clf_indicators"

class IndicatorFeatureVIX(IndicatorFeatureDateBase):
    __tablename__ = "vix_indicators"

class IndicatorFeatureGSPC(IndicatorFeatureDateBase):
    __tablename__ = "gspc_indicators"
