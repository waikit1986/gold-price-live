import yfinance as yf
import pandas as pd
from datetime import timedelta, date
import os


tickers = {
    "GLD": "gld_daily.csv",                # SPDR Gold ETF
    "GC=F": "gold_futures_daily.csv",      # Gold Futures
    "IAU": "iau_daily.csv",                # iShares Gold ETF
    "SI=F": "silver_futures_daily.csv",    # Silver Futures
    "PPLT": "platinum_etf_daily.csv",      # Platinum ETF
    "PALL": "palladium_etf_daily.csv",     # Palladium ETF

    "DX-Y.NYB": "dxy_daily.csv",           # US Dollar Index
    "^TNX": "ten_year_yield_daily.csv",    # 10Y Treasury Yield
    "TIP": "tip_etf_daily.csv",            # TIPS ETF
    "CL=F": "crude_oil_daily.csv",         # Crude Oil

    "^VIX": "vix_daily.csv",               # Volatility Index
    "^GSPC": "sp500_daily.csv",            # S&P 500 Index
}

def download_macro_symbols_all():
    os.makedirs("yfinance/data/daily", exist_ok=True)

    for symbol, filename in tickers.items():
        full_path = os.path.join("yfinance/data/daily", filename)
        print(f"📈 Downloading {symbol}...")

        try:
            if os.path.exists(full_path):
                try:
                    # Skip custom headers manually (assume valid data starts at 4th row)
                    df_existing = pd.read_csv(full_path, skiprows=3, parse_dates=["Date"], index_col="Date")
                    last_date = df_existing.index.max()
                    start_date = min(last_date + timedelta(days=1), pd.Timestamp(date.today()))
                except Exception as e:
                    print(f"⚠️ Old file format incompatible — resetting. ({e})")
                    df_existing = None
                    start_date = "2000-01-01"
            else:
                df_existing = None
                start_date = "2000-01-01"

            # Download new data
            df_new = yf.download(symbol, start=start_date, interval="1d", auto_adjust=True, progress=False)
            if df_new.empty:
                print(f"⚠️ No new data for {symbol}")
                continue

            df_new = df_new[["Open", "High", "Low", "Close", "Volume"]]
            df_new.index.name = "Date"

            if df_existing is not None:
                df_combined = pd.concat([df_existing, df_new])
                df_combined = df_combined[~df_combined.index.duplicated(keep="last")]
                df_combined.sort_index(inplace=True)
            else:
                df_combined = df_new

            # Standard CSV header format
            with open(full_path, "w") as f:
                f.write("Price,Close,High,Low,Open,Volume\n")
                f.write(f"Ticker,{symbol},{symbol},{symbol},{symbol},{symbol}\n")
                f.write("Date,,,,,\n")
                df_combined.to_csv(f, header=False)

            print(f"✅ Updated: {filename} ({len(df_combined)} rows)")

        except Exception as e:
            print(f"❌ Error downloading {symbol}: {e}")

# def download_all():
#     os.makedirs("data/daily", exist_ok=True)
#     for symbol, filename in tickers.items():
#         try:
#             print(f"📈 Downloading {symbol} (1D)...")
#             df = yf.download(symbol, period="max", interval="1d", auto_adjust=True, progress=False)
#             if df.empty:
#                 print(f"⚠️ No data for {symbol}")
#             else:
#                 full_path = os.path.join("yfinance/data/daily", filename)
#                 df.to_csv(full_path)
#                 print(f"✅ Saved: {filename} ({len(df)} rows)")
#         except Exception as e:
#             print(f"❌ Error downloading {symbol}: {e}")

if __name__ == "__main__":
    download_macro_symbols_all()
