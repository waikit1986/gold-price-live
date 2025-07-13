import yfinance as yf
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

def download_all():
    os.makedirs("data/daily", exist_ok=True)
    for symbol, filename in tickers.items():
        try:
            print(f"📈 Downloading {symbol} (1D)...")
            df = yf.download(symbol, period="max", interval="1d", auto_adjust=True, progress=False)
            if df.empty:
                print(f"⚠️ No data for {symbol}")
            else:
                full_path = os.path.join("yfinance/data/daily", filename)
                df.to_csv(full_path)
                print(f"✅ Saved: {filename} ({len(df)} rows)")
        except Exception as e:
            print(f"❌ Error downloading {symbol}: {e}")

if __name__ == "__main__":
    download_all()
