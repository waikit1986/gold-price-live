import sys
import os
import traceback

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from sqlalchemy.orm import Session
from db.database import SessionLocal
from indicators.calculator import compute_indicators

from models_external_symbols import (
    GLD, GCF, IAU, SIF, PPLT, PALL,
    DXY, TNX, TIP, CLF, VIX, GSPC
)

from indicators.models_features import (
    IndicatorFeatureGLD, IndicatorFeatureGCF, IndicatorFeatureIAU,
    IndicatorFeatureSIF, IndicatorFeaturePPLT, IndicatorFeaturePALL,
    IndicatorFeatureDXY, IndicatorFeatureTNX, IndicatorFeatureTIP,
    IndicatorFeatureCLF, IndicatorFeatureVIX, IndicatorFeatureGSPC
)

# Map price & indicator models
price_table_map = {
    "GLD": GLD, "GCF": GCF, "IAU": IAU, "SIF": SIF,
    "PPLT": PPLT, "PALL": PALL, "DXY": DXY, "TNX": TNX,
    "TIP": TIP, "CLF": CLF, "VIX": VIX, "GSPC": GSPC,
}

indicator_model_map = {
    "GLD": IndicatorFeatureGLD, "GCF": IndicatorFeatureGCF, "IAU": IndicatorFeatureIAU,
    "SIF": IndicatorFeatureSIF, "PPLT": IndicatorFeaturePPLT, "PALL": IndicatorFeaturePALL,
    "DXY": IndicatorFeatureDXY, "TNX": IndicatorFeatureTNX, "TIP": IndicatorFeatureTIP,
    "CLF": IndicatorFeatureCLF, "VIX": IndicatorFeatureVIX, "GSPC": IndicatorFeatureGSPC,
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


if __name__ == "__main__":
    generate_all_macro_features()
