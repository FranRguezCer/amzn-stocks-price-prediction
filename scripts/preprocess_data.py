import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# PostgreSQL database connection string
DB_URI = "postgresql://airflow:airflow@airflow_postgres/airflow"

def compute_rsi(series, window=14):
    """Calculate the Relative Strength Index (RSI)."""
    # Compute the daily price changes
    delta = series.diff()
    
    # Separate gains (positive changes) and losses (negative changes)
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    
    # Compute the RSI formula
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def compute_obv(df):
    """Calculate the On-Balance Volume (OBV) indicator."""
    # Determine the direction of price changes (+1 for up, -1 for down, 0 for no change)
    direction = np.sign(df["close"].diff()).fillna(0)
    
    # Compute OBV as a cumulative sum of volume changes based on price movement direction
    return (direction * df["volume"]).cumsum()

def preprocess_data():
    """Process stock data and compute market indicators, storing results in PostgreSQL."""
    engine = create_engine(DB_URI)

    print("🔹 Connecting to PostgreSQL...")
    
    # Load stock data from PostgreSQL into a DataFrame
    df = pd.read_sql("SELECT * FROM stock_data", engine, parse_dates=["date"])

    # Check if data exists
    if df.empty:
        print("❌ Error: No data found in stock_data")
        return

    print(f"✅ {len(df)} rows loaded from stock_data")

    # 🔹 Convert numeric columns to float type
    numeric_cols = ["open", "high", "low", "close", "volume"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

    # Create new features for stock analysis
    df["weekday"] = df["date"].dt.dayofweek  # Day of the week (0 = Monday, 6 = Sunday)
    df["month"] = df["date"].dt.month  # Extract the month
    df["year"] = df["date"].dt.year  # Extract the year
    df["return"] = df["close"].pct_change()  # Compute daily returns
    df["volatility"] = df["return"].rolling(7).std()  # Rolling volatility (7-day window)
    df["sma_7"] = df["close"].rolling(7).mean()  # 7-day Simple Moving Average
    df["sma_14"] = df["close"].rolling(14).mean()  # 14-day Simple Moving Average
    df["rsi"] = compute_rsi(df["close"])  # Calculate RSI
    df["obv"] = compute_obv(df)  # Calculate OBV

    # Display first few rows after preprocessing
    print("🔍 First rows after processing:")
    print(df.head())

    # Remove rows with missing values
    df.dropna(inplace=True)

    # Check if any data remains after removing NaN values
    if df.empty:
        print("⚠ No data remains after removing NaN values")
        return

    # Store the processed data in PostgreSQL
    print(f"📀 Saving {len(df)} rows into the processed_data table...")
    df.to_sql("processed_data", engine, if_exists="replace", index=False)
    print("✅ Processing completed and saved in PostgreSQL")

if __name__ == "__main__":
    preprocess_data()
