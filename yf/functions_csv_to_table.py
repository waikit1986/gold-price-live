import os
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from db.database import SessionLocal
from .models_external_symbols import GLD, GCF, IAU, SIF, PPLT, PALL, DXY, TNX, TIP, CLF, VIX, GSPC


DATA_DIR = "yf/data/daily"
DATABASE_URL = os.getenv("DATABASE_URL")

ticker_to_model = {
    "gld_daily.csv": GLD,
    "gold_futures_daily.csv": GCF,
    "iau_daily.csv": IAU,
    "silver_futures_daily.csv": SIF,
    "platinum_etf_daily.csv": PPLT,
    "palladium_etf_daily.csv": PALL,
    "dxy_daily.csv": DXY,
    "ten_year_yield_daily.csv": TNX,
    "tip_etf_daily.csv": TIP,
    "crude_oil_daily.csv": CLF,
    "vix_daily.csv": VIX,
    "sp500_daily.csv": GSPC,
}

def import_csv_to_db(csv_path: str, model_class, db: Session):
    try:
        df = pd.read_csv(csv_path, skiprows=3)

        if len(df.columns) == 6:
            df.columns = ['date', 'price', 'close', 'high', 'low', 'volume']
            df['open'] = df['low']
            df = df[['date', 'price', 'close', 'high', 'low', 'open', 'volume']]
        else:
            df.columns = ['date', 'price', 'close', 'high', 'low', 'open', 'volume']

        df['date'] = pd.to_datetime(df['date'])
        df['volume'] = df['volume'].fillna(0).astype(int)

        existing_dates = {r[0] for r in db.query(model_class.date).all()}

        new_records = [
            model_class(
                date=row['date'].date(),
                price=row['price'],
                close=row['close'],
                high=row['high'],
                low=row['low'],
                open=row['open'],
                volume=row['volume']
            )
            for _, row in df.iterrows() if row['date'].date() not in existing_dates
        ]

        db.add_all(new_records)
        db.commit()
        print(f"✅ Imported {len(new_records)} rows into '{model_class.__tablename__}' from '{csv_path}'")

    except SQLAlchemyError as e:
        db.rollback()
        print(f"❌ SQLAlchemy error for {csv_path}: {e}")
    except Exception as e:
        print(f"❌ General error for {csv_path}: {e}")

def import_all_csv_to_db():
    with SessionLocal() as db:
        for filename, model_class in ticker_to_model.items():
            filepath = f"{DATA_DIR}/{filename}"
            if os.path.exists(filepath):
                import_csv_to_db(filepath, model_class, db)
            else:
                print(f"⚠️ File not found: {filepath}")

import_all_csv_to_db()
