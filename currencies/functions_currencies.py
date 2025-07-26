from metalpriceapi.client import Client
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from indicators.generate_features import generate_features_for_symbol

from db.database import SessionLocal
from .models_currencies import (
    Xau,
    Xag,
    Xpt,
    Xpd,
    BrentCrude,
    EUR,
    JPY,
    CNY
)

load_dotenv()

api_key = os.getenv("METAL_PRICE_API_KEY")
client = Client(api_key)

symbols_models = {
    "XAU": Xau,
    "XAG": Xag,
    "XPT": Xpt,
    "XPD": Xpd,
    "BRENT-CRUDE": BrentCrude,
    "EUR": EUR,
    "JPY": JPY,
    "CNY": CNY,
}

def get_currencies():
    db: Session = None
    try:
        symbols = list(symbols_models.keys())

        result = client.fetchLive(base='USD', currencies=symbols)

        print("📦 API response:", result)

        if not result.get("success", False):
            raise ValueError("API call unsuccessful")

        if "timestamp" not in result:
            raise KeyError("Missing 'timestamp' in API response")

        rates = result.get("rates", {})
        timestamp = datetime.fromtimestamp(result["timestamp"], tz=timezone.utc)

        db = SessionLocal()

        for symbol, model in symbols_models.items():
            price = rates.get(symbol)
            if price is not None:
                exists = db.query(model).filter(model.timestamp == timestamp).first()
                if exists:
                    print(f"⏭️ {symbol} at {timestamp} already exists, skipping insert.")
                else:
                    db.add(model(timestamp=timestamp, price=price))
                    print(f"➕ Added {symbol} at {timestamp} with price {price}")

        db.commit()
        print("✅ Data saved to database successfully.")

        for symbol, model in symbols_models.items():
            exists = db.query(model).filter(model.timestamp == timestamp).first()
            if exists:
                print(f"⏭️ {symbol} indicators at {timestamp} already exists, skipping insert.")
            else:
                generate_features_for_symbol(symbol, model, timeframe="1T")

    except Exception as e:
        print(f"❌ Error fetching/saving metal prices: {e}")

    finally:
        if db:
            db.close()
