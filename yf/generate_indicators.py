import traceback
import pandas as pd
from sqlalchemy.orm import Session

from db.database import SessionLocal
from indicators.calculator import compute_indicators

# database models
from .models_external_symbols import (
    GLD, GCF, IAU, SIF, PPLT, PALL,
    DXY, TNX, TIP, CLF, VIX, GSPC
)

# indicator models
from indicators.models_features import (
    IndicatorFeatureGCF_1D,
    IndicatorFeatureIAU_1D,
    IndicatorFeaturePALL_1D,
    IndicatorFeaturePPLT_1D,
    IndicatorFeatureBrentCrude_1D,
    IndicatorFeatureCNY_1D,
    IndicatorFeatureEUR_1D,
    IndicatorFeatureJPY_1D,
    IndicatorFeatureXAG_1D,
    IndicatorFeatureXAU_1D,
    IndicatorFeatureXPD_1D,
    IndicatorFeatureXPT_1D,
    IndicatorFeatureCLF_1D,
    IndicatorFeatureDXY_1D,
    IndicatorFeatureGLD_1D,
    IndicatorFeatureGSPC_1D,
    IndicatorFeatureTIP_1D,
    IndicatorFeatureTNX_1D,
    IndicatorFeatureVIX_1D,
    IndicatorFeatureSIF_1D,
)

# Map price & indicator models
price_table_map = {
    "GLD_1D": GLD, "GCF_1D": GCF, "IAU_1D": IAU, "SIF_1D": SIF,
    "PPLT_1D": PPLT, "PALL_1D": PALL, "DXY_1D": DXY, "TNX_1D": TNX,
    "TIP_1D": TIP, "CLF_1D": CLF, "VIX_1D": VIX, "GSPC_1D": GSPC,
}

indicator_model_map = {
"GLD_1D": IndicatorFeatureGLD_1D,
"GCF_1D": IndicatorFeatureGCF_1D,
"IAU_1D": IndicatorFeatureIAU_1D,
"SIF_1D": IndicatorFeatureSIF_1D,
"PPLT_1D": IndicatorFeaturePPLT_1D,
"PALL_1D": IndicatorFeaturePALL_1D,
"BrentCrude_1D": IndicatorFeatureBrentCrude_1D,
"CNY_1D": IndicatorFeatureCNY_1D,
"EUR_1D": IndicatorFeatureEUR_1D,
"JPY_1D": IndicatorFeatureJPY_1D,
"XAG_1D": IndicatorFeatureXAG_1D,
"XAU_1D": IndicatorFeatureXAU_1D,
"XPD_1D": IndicatorFeatureXPD_1D,
"XPT_1D": IndicatorFeatureXPT_1D,
"CLF_1D": IndicatorFeatureCLF_1D,
"DXY_1D": IndicatorFeatureDXY_1D,
"GLD_1D": IndicatorFeatureGLD_1D,
"GSPC_1D": IndicatorFeatureGSPC_1D,
"TIP_1D": IndicatorFeatureTIP_1D,
"TNX_1D": IndicatorFeatureTNX_1D,
"VIX_1D": IndicatorFeatureVIX_1D,
"SIF_1D": IndicatorFeatureSIF_1D,
}


def fetch_price_data(session: Session, table_model, timeframe: str) -> pd.DataFrame:
    """Fetch and resample price data."""
    rows = session.query(table_model).order_by(table_model.date).all()

    df = pd.DataFrame([
        {"time": r.date, "price": r.price}
        for r in rows
    ])

    df["time"] = pd.to_datetime(df["time"])
    df.set_index("time", inplace=True)

    timeframe_fixed = timeframe.replace("T", "min")
    df_resampled = df.resample(timeframe_fixed).last().dropna()

    return df_resampled

def generate_features_for_symbol(symbol: str, price_model, indicator_model, timeframe: str = "1D"):
    """Generate technical indicator features and insert into DB."""
    session = SessionLocal()
    try:
        df = fetch_price_data(session, price_model, timeframe)
        df = compute_indicators(df)

        existing_keys = {
            (row[0], row[1]) for row in
            session.query(indicator_model.date, indicator_model.indicator).distinct()
        }

        inserted_count = 0

        for time_idx, row in df.iterrows():
            date_val = time_idx.date()

            for indicator_name in df.columns:
                if indicator_name == "price":
                    continue

                if (date_val, indicator_name) in existing_keys:
                    continue

                value = row[indicator_name]
                if pd.notnull(value):
                    feature = indicator_model(
                        date=date_val,
                        price=float(row["price"]),
                        indicator=indicator_name,
                        value=float(value)
                    )
                    session.add(feature)
                    inserted_count += 1

        session.commit()
        print(f"✅ {symbol}: Inserted {inserted_count} new indicator rows.")

    except Exception as e:
        print(f"❌ {symbol}: Error - {e}")
        traceback.print_exc()
    finally:
        session.close()

def generate_all_macro_features(timeframe: str = "1D"):
    """Generate features for all mapped macro symbols."""
    for symbol in price_table_map:
        print(f"▶️ Generating features for {symbol} with timeframe {timeframe}...")
        generate_features_for_symbol(
            symbol,
            price_model=price_table_map[symbol],
            indicator_model=indicator_model_map[symbol],
            timeframe=timeframe
        )

generate_all_macro_features()
