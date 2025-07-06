import yfinance as yf

def get_yfinance_data(ticker):
    try:
        data = yf.download(ticker, period="730d", interval="1h")
        print(data)
        data.to_csv("gld_hourly.csv")
    except Exception as e:
        print(f"Error fetching yfinance data: {e}")

get_yfinance_data("GC=F")

