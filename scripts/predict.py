import pandas as pd
import joblib
from sqlalchemy import create_engine

# PostgreSQL database connection string
DB_URI = "postgresql://airflow:airflow@airflow_postgres/airflow"

# Path to the trained model file
MODEL_FILE = "models/amzn_model.pkl"

def predict():
    """Generate AMZN stock price predictions using the trained model and store them in PostgreSQL."""
    engine = create_engine(DB_URI)

    # Load the trained model from file
    model = joblib.load(MODEL_FILE)

    # Load the preprocessed stock data from PostgreSQL
    df = pd.read_sql("SELECT * FROM processed_data", engine, parse_dates=["date"])

    # Generate stock price predictions using the trained model
    df["predicted_close"] = model.predict(df[[
        "open", "high", "low", "volume", "weekday", "month", "year", "return",
        "volatility", "sma_7", "sma_14", "rsi", "obv"
    ]])

    # Store the predictions in PostgreSQL
    df[["date", "close", "predicted_close"]].to_sql("predictions", engine, if_exists="replace", index=False)

    print("✅ Predictions stored in PostgreSQL (table: predictions)")

if __name__ == "__main__":
    predict()
