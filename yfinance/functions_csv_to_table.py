import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/..")))
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from db.database import SessionLocal
from models_external_symbols import GLD, GCF, IAU, SIF, PPLT, PALL, DXY, TNX, TIP, CLF, VIX, GSPC


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

DATA_DIR = "yfinance/data/daily"
DATABASE_URL = os.getenv("DATABASE_URL")


def import_csv_to_db(csv_path: str, model_class, db: Session):
    try:
        # Read the file, skipping first 3 metadata rows
        df = pd.read_csv(csv_path, skiprows=3)

        # Handle column mismatch (6 or 7 columns)
        if len(df.columns) == 6:
            df.columns = ['date', 'price', 'close', 'high', 'low', 'volume']
            df['open'] = df['low']  # or df['price']
            df = df[['date', 'price', 'close', 'high', 'low', 'open', 'volume']]
        else:
            df.columns = ['date', 'price', 'close', 'high', 'low', 'open', 'volume']

        df['date'] = pd.to_datetime(df['date'])
        df['volume'] = df['volume'].fillna(0).astype(int)

        existing_dates = {
            row[0] for row in db.query(model_class.date).all()
        }

        imported_count = 0

        for _, row in df.iterrows():
            row_date = row['date'].date()

            if row_date in existing_dates:
                continue

            record = model_class(
                date=row_date,
                price=row['price'],
                close=row['close'],
                high=row['high'],
                low=row['low'],
                open=row['open'],
                volume=row['volume']
            )
            db.add(record)
            imported_count += 1

        db.commit()
        print(f"✅ Imported {imported_count} new rows into '{model_class.__tablename__}' from '{csv_path}'")

    except SQLAlchemyError as e:
        db.rollback()
        print(f"❌ SQLAlchemy error for {csv_path}: {e}")
    except Exception as e:
        print(f"❌ General error for {csv_path}: {e}")


def import_all():
    with SessionLocal() as db:
        for filename, model_class in ticker_to_model.items():
            path = os.path.join(DATA_DIR, filename)
            if os.path.exists(path):
                import_csv_to_db(path, model_class, db)
            else:
                print(f"⚠️ File not found: {path}")


if __name__ == "__main__":
    import_all()
