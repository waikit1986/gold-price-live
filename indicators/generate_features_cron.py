import pandas as pd
from sqlalchemy.orm import Session
from db.database import SessionLocal
from indicators.calculator import compute_indicators
from indicators.models_features import (
    IndicatorFeatureXau, IndicatorFeatureXag,
    IndicatorFeatureXpt, IndicatorFeatureXpd,
    IndicatorFeatureBrentCrude, IndicatorFeatureEur,
    IndicatorFeatureJpy, IndicatorFeatureCny
)

indicator_model_map = {
    "XAU": IndicatorFeatureXau,
    "XAG": IndicatorFeatureXag,
    "XPT": IndicatorFeatureXpt,
    "XPD": IndicatorFeatureXpd,
    "BRENT-CRUDE": IndicatorFeatureBrentCrude,
    "EUR": IndicatorFeatureEur,
    "JPY": IndicatorFeatureJpy,
    "CNY": IndicatorFeatureCny,
}

def fetch_price_data(session: Session, table_model, timeframe: str) -> pd.DataFrame:
    rows = session.query(table_model).order_by(table_model.timestamp).all()
    df = pd.DataFrame([{"timestamp": r.timestamp, "price": r.price} for r in rows])
    df.set_index("timestamp", inplace=True)
    # Fix FutureWarning by replacing 'T' with 'min'
    timeframe_fixed = timeframe.replace('T', 'min')
    df_resampled = df.resample(timeframe_fixed).last().dropna()
    return df_resampled

def generate_features_for_symbol(symbol: str, table_model, timeframe: str):
    session = SessionLocal()
    try:
        df = fetch_price_data(session, table_model, timeframe)

        # Compute all indicators (including your expanded set)
        df = compute_indicators(df)

        IndicatorFeatureModel = indicator_model_map.get(symbol)
        if not IndicatorFeatureModel:
            print(f"⚠️ No indicator model found for symbol {symbol}")
            return

        for timestamp, row in df.iterrows():
            # For each indicator column (skip 'price')
            for indicator_name in df.columns:
                if indicator_name == "price":
                    continue
                value = row[indicator_name]
                if pd.notnull(value):
                    feature = IndicatorFeatureModel(
                        timestamp=timestamp.to_pydatetime(),
                        price=float(row["price"]),       
                        indicator=indicator_name,
                        value=float(value)                
                    )
                    session.merge(feature)

        session.commit()
        print(f"✅ Features for {symbol} generated and saved successfully.")
    except Exception as e:
        print(f"❌ Error generating features for {symbol}: {e}")
    finally:
        session.close()
