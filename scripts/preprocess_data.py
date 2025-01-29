import pandas as pd
import numpy as np

INPUT_FILE = "data/extracted_data.csv"
OUTPUT_FILE = "data/processed_data.csv"

def compute_rsi(series, window=14):
    """Calculate Relative Strength Index (RSI)."""
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def compute_obv(df):
    """Calculate On-Balance Volume (OBV)."""
    direction = np.sign(df["close"].diff()).fillna(0)
    return (direction * df["volume"]).cumsum()

def preprocess_data():
    """Process stock data and compute market indicators."""
    df = pd.read_csv(INPUT_FILE, index_col=0, parse_dates=True)
    df = df.astype(float)

    # Date-based features
    df["weekday"] = df.index.dayofweek
    df["month"] = df.index.month
    df["year"] = df.index.year

    # Returns & Volatility
    df["return"] = df["close"].pct_change()
    df["volatility"] = df["return"].rolling(7).std()

    # Moving Averages
    df["sma_7"] = df["close"].rolling(7).mean()
    df["sma_14"] = df["close"].rolling(14).mean()

    # RSI & OBV
    df["rsi"] = compute_rsi(df["close"])
    df["obv"] = compute_obv(df)

    df.dropna(inplace=True)  # Drop rows with NaN from rolling calculations
    df.to_csv(OUTPUT_FILE)

    print(f"✅ Processed data saved: {OUTPUT_FILE}")

if __name__ == "__main__":
    preprocess_data()
