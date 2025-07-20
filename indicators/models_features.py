from sqlalchemy import Column, Date, DateTime, Float, String
from db.database import Base

# Shared base classes
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


# === 1H Timestamp-Based Models ===
class IndicatorFeatureXAU_1H(IndicatorFeatureTimeStampBase):
    __tablename__ = "xau_indicators_1h"

class IndicatorFeatureXAG_1H(IndicatorFeatureTimeStampBase):
    __tablename__ = "xag_indicators_1h"

class IndicatorFeatureXPT_1H(IndicatorFeatureTimeStampBase):
    __tablename__ = "xpt_indicators_1h"

class IndicatorFeatureXPD_1H(IndicatorFeatureTimeStampBase):
    __tablename__ = "xpd_indicators_1h"

class IndicatorFeatureBrentCrude_1H(IndicatorFeatureTimeStampBase):
    __tablename__ = "brent_crude_indicators_1h"

class IndicatorFeatureEUR_1H(IndicatorFeatureTimeStampBase):
    __tablename__ = "eur_indicators_1h"

class IndicatorFeatureJPY_1H(IndicatorFeatureTimeStampBase):
    __tablename__ = "jpy_indicators_1h"

class IndicatorFeatureCNY_1H(IndicatorFeatureTimeStampBase):
    __tablename__ = "cny_indicators_1h"

class IndicatorFeatureGLD_1H(IndicatorFeatureTimeStampBase):
    __tablename__ = "gld_indicators_1h"

class IndicatorFeatureGCF_1H(IndicatorFeatureTimeStampBase):
    __tablename__ = "gcf_indicators_1h"

class IndicatorFeatureIAU_1H(IndicatorFeatureTimeStampBase):
    __tablename__ = "iau_indicators_1h"

class IndicatorFeatureSIF_1H(IndicatorFeatureTimeStampBase):
    __tablename__ = "sif_indicators_1h"

class IndicatorFeaturePPLT_1H(IndicatorFeatureTimeStampBase):
    __tablename__ = "pplt_indicators_1h"

class IndicatorFeaturePALL_1H(IndicatorFeatureTimeStampBase):
    __tablename__ = "pall_indicators_1h"

class IndicatorFeatureDXY_1H(IndicatorFeatureTimeStampBase):
    __tablename__ = "dxy_indicators_1h"

class IndicatorFeatureTNX_1H(IndicatorFeatureTimeStampBase):
    __tablename__ = "tnx_indicators_1h"

class IndicatorFeatureTIP_1H(IndicatorFeatureTimeStampBase):
    __tablename__ = "tip_indicators_1h"

class IndicatorFeatureCLF_1H(IndicatorFeatureTimeStampBase):
    __tablename__ = "clf_indicators_1h"

class IndicatorFeatureVIX_1H(IndicatorFeatureTimeStampBase):
    __tablename__ = "vix_indicators_1h"

class IndicatorFeatureGSPC_1H(IndicatorFeatureTimeStampBase):
    __tablename__ = "gspc_indicators_1h"


# === 1D Date-Based Models ===
class IndicatorFeatureXAU_1D(IndicatorFeatureDateBase):
    __tablename__ = "xau_indicators_1d"

class IndicatorFeatureXAG_1D(IndicatorFeatureDateBase):
    __tablename__ = "xag_indicators_1d"

class IndicatorFeatureXPT_1D(IndicatorFeatureDateBase):
    __tablename__ = "xpt_indicators_1d"

class IndicatorFeatureXPD_1D(IndicatorFeatureDateBase):
    __tablename__ = "xpd_indicators_1d"

class IndicatorFeatureBrentCrude_1D(IndicatorFeatureDateBase):
    __tablename__ = "brent_crude_indicators_1d"

class IndicatorFeatureEUR_1D(IndicatorFeatureDateBase):
    __tablename__ = "eur_indicators_1d"

class IndicatorFeatureJPY_1D(IndicatorFeatureDateBase):
    __tablename__ = "jpy_indicators_1d"

class IndicatorFeatureCNY_1D(IndicatorFeatureDateBase):
    __tablename__ = "cny_indicators_1d"

class IndicatorFeatureGLD_1D(IndicatorFeatureDateBase):
    __tablename__ = "gld_indicators_1d"

class IndicatorFeatureGCF_1D(IndicatorFeatureDateBase):
    __tablename__ = "gcf_indicators_1d"

class IndicatorFeatureIAU_1D(IndicatorFeatureDateBase):
    __tablename__ = "iau_indicators_1d"

class IndicatorFeatureSIF_1D(IndicatorFeatureDateBase):
    __tablename__ = "sif_indicators_1d"

class IndicatorFeaturePPLT_1D(IndicatorFeatureDateBase):
    __tablename__ = "pplt_indicators_1d"

class IndicatorFeaturePALL_1D(IndicatorFeatureDateBase):
    __tablename__ = "pall_indicators_1d"

class IndicatorFeatureDXY_1D(IndicatorFeatureDateBase):
    __tablename__ = "dxy_indicators_1d"

class IndicatorFeatureTNX_1D(IndicatorFeatureDateBase):
    __tablename__ = "tnx_indicators_1d"

class IndicatorFeatureTIP_1D(IndicatorFeatureDateBase):
    __tablename__ = "tip_indicators_1d"

class IndicatorFeatureCLF_1D(IndicatorFeatureDateBase):
    __tablename__ = "clf_indicators_1d"

class IndicatorFeatureVIX_1D(IndicatorFeatureDateBase):
    __tablename__ = "vix_indicators_1d"

class IndicatorFeatureGSPC_1D(IndicatorFeatureDateBase):
    __tablename__ = "gspc_indicators_1d"
