import requests
import pandas as pd

API_KEY = "your_API_key_here"
SYMBOL = "AMZN"
OUTPUT_FILE = "data/extracted_data.csv"

def extract_data():
    """Fetch AMZN stock data from Alpha Vantage API."""
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": SYMBOL,
        "apikey": API_KEY,
        "outputsize": "full",
        "datatype": "json"
    }

    data = requests.get(url, params=params).json()
    if "Time Series (Daily)" not in data:
        print("❌ API error")
        return

    df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index")
    df = df.rename(columns={
        "1. open": "open", "2. high": "high",
        "3. low": "low", "4. close": "close",
        "5. volume": "volume"
    })

    df.index = pd.to_datetime(df.index)
    df.sort_index().to_csv(OUTPUT_FILE)
    print(f"✅ Data saved: {OUTPUT_FILE}")

if __name__ == "__main__":
    extract_data()
