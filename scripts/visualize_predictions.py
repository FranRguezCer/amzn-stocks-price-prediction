import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Database connection string
DB_URI = "postgresql://airflow:airflow@airflow_postgres/airflow"
# Output file path for the visualization
OUTPUT_FILE = "/opt/airflow/plots/amzn_predictions.png"

def visualize_predictions():
    """Generate a plot comparing actual vs predicted AMZN stock prices using PostgreSQL data."""
    # Connect to PostgreSQL
    engine = create_engine(DB_URI)

    # Load predictions data from PostgreSQL
    predictions_df = pd.read_sql("SELECT * FROM predictions", engine, parse_dates=["date"])
    print(f"Loaded {len(predictions_df)} rows from predictions table.")

    # Load model metrics from PostgreSQL
    metrics_df = pd.read_sql("SELECT * FROM model_metrics", engine)
    metrics_text = "\n".join([f"{row['metric']}: {row['value']:.4f}" for _, row in metrics_df.iterrows()])
    print("Model metrics loaded:", metrics_text)

    # Create the plot
    plt.figure(figsize=(14, 7))
    plt.plot(predictions_df["date"], predictions_df["close"], label="Actual", color="navy", linewidth=1.5)
    plt.plot(predictions_df["date"], predictions_df["predicted_close"], label="Predicted", color="darkorange", linestyle="dashed", linewidth=1.5)

    # Shade the area under the curves
    plt.fill_between(predictions_df["date"], predictions_df["close"], alpha=0.2, color="navy")
    plt.fill_between(predictions_df["date"], predictions_df["predicted_close"], alpha=0.2, color="darkorange")

    # Set labels and title
    plt.xlabel("Date", fontsize=14)
    plt.ylabel("Closing Price", fontsize=14)
    plt.title("AMZN Stock Price Prediction vs Actual Values", fontsize=16, fontweight="bold")

    # Display model metrics as a text box in the center
    plt.text(0.5, 0.90, metrics_text, fontsize=12, ha="center", va="top", transform=plt.gca().transAxes, bbox=dict(facecolor="white", alpha=0.7))

    # Add grid for better readability
    plt.grid(True, linestyle="--", alpha=0.6)

    # Show legend
    plt.legend()

    # Save the plot to a file
    plt.savefig(OUTPUT_FILE, dpi=300)
    print(f"✅ Visualization saved at: {OUTPUT_FILE}")

if __name__ == "__main__":
    visualize_predictions()
