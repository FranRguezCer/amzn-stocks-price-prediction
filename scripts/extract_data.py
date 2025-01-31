import requests
import pandas as pd
from sqlalchemy import create_engine

# API key for Alpha Vantage
API_KEY = "your_API_key"
# Stock symbol to fetch data for
SYMBOL = "AMZN"
# PostgreSQL database connection string
DB_URI = "postgresql://airflow:airflow@airflow_postgres/airflow"

def extract_data():
    """Fetch AMZN stock data from Alpha Vantage API and store it in PostgreSQL."""
    
    # API endpoint and parameters for retrieving historical daily stock prices
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",  # Request daily stock prices
        "symbol": SYMBOL,  # Stock ticker symbol
        "apikey": API_KEY,  # API authentication key
        "outputsize": "full",  # Fetch full historical data
        "datatype": "json"  # Response format
    }

    # Send GET request to the API and parse the response as JSON
    data = requests.get(url, params=params).json()

    # Check if the expected data key exists in the response
    if "Time Series (Daily)" not in data:
        print("❌ API error")  # Log an error if data is not retrieved
        return

    # Convert the API response into a pandas DataFrame
    df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index")

    # Rename columns to more readable names
    df = df.rename(columns={
        "1. open": "open", "2. high": "high",
        "3. low": "low", "4. close": "close",
        "5. volume": "volume"
    })

    # Convert the index (which contains dates) to datetime format
    df.index = pd.to_datetime(df.index)

    # Sort data chronologically and reset index, renaming it to "date"
    df = df.sort_index().reset_index().rename(columns={"index": "date"})

    # Store the data in PostgreSQL
    engine = create_engine(DB_URI)
    df.to_sql("stock_data", engine, if_exists="replace", index=False)

    print("✅ Data stored in PostgreSQL (table: stock_data)")

if __name__ == "__main__":
    extract_data()
