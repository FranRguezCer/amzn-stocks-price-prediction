from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import pandas as pd

# File paths
INPUT_FILE = "data/processed_data.csv"
MODEL_FILE = "models/amzn_model.pkl"
METRICS_FILE = "data/model_metrics.csv"

def train_model():
    """Train HGBR model with test evaluation only."""
    df = pd.read_csv(INPUT_FILE, index_col=0)

    # Define features and target
    X = df[["open", "high", "low", "volume", "weekday", "month", "year", "return",
            "volatility", "sma_7", "sma_14", "rsi", "obv"]]
    y = df["close"]

    # Train-test split (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Hyperparameter tuning
    param_grid = {
        "max_iter": [75, 100],  
        "max_depth": [3, 4],  
        "learning_rate": [0.01, 0.001],  
        "min_samples_leaf": [30, 60],  
        "l2_regularization": [0.1, 0.5]  
    }

    model = GridSearchCV(HistGradientBoostingRegressor(random_state=42), param_grid,
                         cv=5, scoring="neg_mean_squared_error", n_jobs=-1)
    model.fit(X_train, y_train)

    # Best model
    best_model = model.best_estimator_
    joblib.dump(best_model, MODEL_FILE)
    print(f"✅ Model saved: {MODEL_FILE}")

    # Evaluate on test set only
    y_test_pred = best_model.predict(X_test)

    # Compute test metrics
    test_r2 = r2_score(y_test, y_test_pred)
    test_mse = mean_squared_error(y_test, y_test_pred)
    test_mae = mean_absolute_error(y_test, y_test_pred)

    # Save test metrics
    metrics = pd.DataFrame({
        "Metric": ["R²", "MSE", "MAE"],
        "Value": [test_r2, test_mse, test_mae]
    })
    metrics.to_csv(METRICS_FILE, index=False)
    
    print(f"📊 Test Performance:\n"
          f"R²: {test_r2:.4f}, MSE: {test_mse:.4f}, MAE: {test_mae:.4f}")
    print(f"✅ Metrics saved: {METRICS_FILE}")

if __name__ == "__main__":
    train_model()
