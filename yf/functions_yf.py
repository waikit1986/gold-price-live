import yfinance as yf


tickers = {
    "GLD": "yfinance/data/daily/gld_daily.csv",
    "GC=F": "yfinance/data/daily/gold_futures_daily.csv",
    "IAU": "yfinance/data/daily/iau_daily.csv",
    "SI=F": "yfinance/data/daily/silver_futures_daily.csv",
    "PPLT": "yfinance/data/daily/platinum_etf_daily.csv",
    "PALL": "yfinance/data/daily/palladium_etf_daily.csv",
    "DX-Y.NYB": "yfinance/data/daily/dxy_daily.csv",
    "^TNX": "yfinance/data/daily/ten_year_yield_daily.csv",
    "TIP": "yfinance/data/daily/tip_etf_daily.csv",
    "CL=F": "yfinance/data/daily/crude_oil_daily.csv",
    "^VIX": "yfinance/data/daily/vix_daily.csv",
    "^GSPC": "yfinance/data/daily/sp500_daily.csv",
}

def download_macro_symbols_all():
    for symbol, filepath in tickers.items():
        print(f"📈 Downloading {symbol}...")
        try:
            df = yf.download(symbol, start="2000-01-01", interval="1d", auto_adjust=True, progress=False)
            if df.empty:
                print(f"⚠️ No data for {symbol}")
                continue

            df = df[["Open", "High", "Low", "Close", "Volume"]]
            df.index.name = "Date"

            with open(filepath, "w") as f:
                f.write("Price,Close,High,Low,Open,Volume\n")
                f.write(f"Ticker,{symbol},{symbol},{symbol},{symbol},{symbol}\n")
                f.write("Date,,,,,\n")
                df.to_csv(f, header=False)

            print(f"✅ Saved: {filepath} ({len(df)} rows)")
        except Exception as e:
            print(f"❌ Error downloading {symbol}: {e}")

download_macro_symbols_all()
