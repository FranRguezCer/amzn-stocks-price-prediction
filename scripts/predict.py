import pandas as pd
import joblib
import os

# File paths
MODEL_FILE = "models/amzn_model.pkl"
INPUT_FILE = "data/processed_data.csv"
OUTPUT_FILE = "data/predictions.csv"

def predict():
    """Generate AMZN stock price predictions using the trained model."""
    
    # Check if necessary files exist
    if not os.path.exists(MODEL_FILE):
        print("❌ Model not found.")
        return
    if not os.path.exists(INPUT_FILE):
        print("❌ Processed data not found.")
        return

    # Load processed data
    df = pd.read_csv(INPUT_FILE, index_col=0)
    
    # Load trained model
    model = joblib.load(MODEL_FILE)

    # Predict closing price using all engineered features
    df["predicted_close"] = model.predict(df[[
        "open", "high", "low", "volume", "weekday", "month", "year", "return",
        "volatility", "sma_7", "sma_14", "rsi", "obv"
    ]])

    # Save predictions alongside actual closing prices
    df[["close", "predicted_close"]].to_csv(OUTPUT_FILE)

    print(f"✅ Predictions saved: {OUTPUT_FILE}")

if __name__ == "__main__":
    predict()
