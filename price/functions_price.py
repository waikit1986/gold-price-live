from metalpriceapi.client import Client
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("METAL_PRICE_API_KEY")
client = Client(api_key)

def get_metal_price():
    try:
        result = client.timeframe(start_date='1974-06-06', end_date='2025-07-04', currencies=['XAU'])
        print(result)
    except Exception as e:
        print(f"Error fetching metal prices: {e}")
        
get_metal_price()
