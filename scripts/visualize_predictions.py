import pandas as pd
import matplotlib.pyplot as plt
import os

# File paths
PREDICTIONS_FILE = "data/predictions.csv"
METRICS_FILE = "data/model_metrics.csv"
OUTPUT_FILE = "data/plots/amzn_predictions.png"

def visualize_predictions():
    """Generate a plot of actual vs predicted AMZN stock prices with model metrics."""
    
    # Check if required files exist
    if not os.path.exists(PREDICTIONS_FILE):
        print("❌ Predictions file not found.")
        return
    if not os.path.exists(METRICS_FILE):
        print("❌ Model metrics file not found.")
        return

    # Load predictions
    df = pd.read_csv(PREDICTIONS_FILE, index_col=0, parse_dates=True)

    # Load model metrics
    metrics_df = pd.read_csv(METRICS_FILE)
    metrics_text = "\n".join([f"{row['Metric']}: {row['Value']:.4f}" for _, row in metrics_df.iterrows()])

    # Create plot
    plt.figure(figsize=(14, 7))

    # Actual values (navy)
    plt.plot(df.index, df["close"], label="Real", color="navy", linewidth=2)
    plt.fill_between(df.index, df["close"], alpha=0.6, color="navy")

    # Predicted values (darkorange, dashed)
    plt.plot(df.index, df["predicted_close"], label="Predicted", color="darkorange", linestyle="dashed", linewidth=2)
    plt.fill_between(df.index, df["predicted_close"], alpha=0.6, color="darkorange")

    # Grid, labels, and title
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.xlabel("Date")
    plt.ylabel("AMZN Closing Price")
    plt.title("AMZN Stock Price Prediction (Real vs Predicted)")
    plt.legend()

    # Add model metrics as text in the top center of the plot
    plt.text(0.5, 0.85, metrics_text, fontsize=10, transform=plt.gca().transAxes,
             bbox=dict(facecolor='white', alpha=0.7), ha="center")

    # Save the plot
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    plt.savefig(OUTPUT_FILE)

    print(f"✅ Visualization saved: {OUTPUT_FILE}")

if __name__ == "__main__":
    visualize_predictions()
