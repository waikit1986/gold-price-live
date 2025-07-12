import yfinance as yf
import os

tickers = {
    "GC=F": "gold_futures_1H.csv",              # Gold Futures
    "SI=F": "silver_futures_1H.csv",            # Silver Futures
    "IAU": "iau_1H.csv",                        # iShares Gold ETF
    "GLD": "gld_1H.csv",                        # SPDR Gold ETF
    "GDX": "gdx_1H.csv",                        # Gold Miners ETF
    "NEM": "newmont_1H.csv",                    # Newmont Corporation

    "^TNX": "ten_year_yield_1H.csv",            # 10-Year Treasury Yield
    "^IRX": "three_month_yield_1H.csv",         # 13-Week Treasury Yield
    "TIP": "tip_1H.csv",                        # TIPS ETF

    "DX-Y.NYB": "dxy_1H.csv",                   # US Dollar Index
    "EURUSD=X": "eur_usd_1H.csv",               # EUR/USD FX Pair
    "USDCNY=X": "usdcny_1H.csv",                # USD/CNY FX Pair

    "^GSPC": "sp500_1H.csv",                    # S&P 500 Index
    "^IXIC": "nasdaq_1H.csv",                   # Nasdaq Index
    "SPY": "spy_1H.csv",                        # S&P 500 ETF
    "XLF": "xlf_1H.csv",                        # Financial Sector ETF

    "^VIX": "vix_1H.csv",                       # Volatility Index
    "CL=F": "crude_oil_1H.csv",                 # Crude Oil Futures
    "HG=F": "copper_futures_1H.csv",            # Copper Futures
}

def download_all():
    os.makedirs("data", exist_ok=True)
    for symbol, filename in tickers.items():
        try:
            print(f"📈 Fetching {symbol} (1H, max)...")
            df = yf.download(symbol, period="max", interval="1h", auto_adjust=True, progress=False)
            if df.empty:
                print(f"⚠️ No data for {symbol}")
            else:
                full_path = os.path.join("data/1H", filename)
                df.to_csv(full_path)
                print(f"✅ Saved: {filename} ({len(df)} rows)")
        except Exception as e:
            print(f"❌ Error fetching {symbol}: {e}")

if __name__ == "__main__":
    download_all()



# import yfinance as yf

# # Ticker symbol to filename mapping
# tickers = {
#     "GLD": "gld_hourly.csv",
#     "XAUUSD=X": "xauusd_hourly.csv",
#     "GC=F": "gold_futures_hourly.csv",
#     "IAU": "iau_hourly.csv",
#     "SGOL": "sgol_hourly.csv",
#     "PHYS": "phys_hourly.csv",
#     "GDX": "gdx_hourly.csv",
#     "GDXJ": "gdxj_hourly.csv",
#     "SLV": "slv_hourly.csv",
#     "PPLT": "pplt_hourly.csv",
#     "^TNX": "ten_year_yield_hourly.csv",
#     "DX-Y.NYB": "dxy_hourly.csv",
#     "^GSPC": "sp500_hourly.csv",
#     "^VIX": "vix_hourly.csv",
#     "CL=F": "crude_oil_hourly.csv",
#     "BTC-USD": "btc_usd_hourly.csv",
#     "USDCNY=X": "usdcny_hourly.csv"
# }

# def get_yfinance_data(ticker, filename):
#     try:
#         print(f"Fetching {ticker}...")
#         df = yf.download(ticker, period="730d", interval="1h", progress=False)
#         if not df.empty:
#             df.to_csv(filename)
#             print(f"Saved: {filename}")
#         else:
#             print(f"No data for {ticker}")
#     except Exception as e:
#         print(f"Error fetching {ticker}: {e}")

# def download_all():
#     for symbol, filename in tickers.items():
#         get_yfinance_data(symbol, filename)

# if __name__ == "__main__":
#     download_all()


# import yfinance as yf

# def get_yfinance_data(ticker):
#     try:
#         data = yf.download(ticker, period="max", interval="1d")
#         print(data)
#         data.to_csv("gld_daily.csv")
#     except Exception as e:
#         print(f"Error fetching yfinance data: {e}")

# get_yfinance_data("GLD")


# import yfinance as yf

# def get_yfinance_data(ticker):
#     try:
#         data = yf.download(ticker, period="730d", interval="1h")
#         print(data)
#         data.to_csv("gld_hourly.csv")
#     except Exception as e:
#         print(f"Error fetching yfinance data: {e}")

# get_yfinance_data("GC=F")

