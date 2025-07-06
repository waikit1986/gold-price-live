import yfinance as yf

def get_yfinance_data(ticker):
    try:
        data = yf.download("GC=F", start="1974-01-01", end="2025-07-06", interval="1d")
        print(data)
        data.to_csv("gld_historical_daily_data.csv")
    except Exception as e:
        print(f"Error fetching yfinance data: {e}")

get_yfinance_data("GC=F")