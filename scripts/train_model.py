from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL database connection string
DB_URI = "postgresql://airflow:airflow@airflow_postgres/airflow"

# Path to save the trained model
MODEL_FILE = "models/amzn_model.pkl"

def train_model():
    """Train an HGBR model using data from PostgreSQL and store performance metrics in the database."""
    engine = create_engine(DB_URI)

    # Load preprocessed stock data from PostgreSQL
    df = pd.read_sql("SELECT * FROM processed_data", engine, parse_dates=["date"])

    # Define feature set (X) and target variable (y)
    X = df[["open", "high", "low", "volume", "weekday", "month", "year", "return",
            "volatility", "sma_7", "sma_14", "rsi", "obv"]]
    y = df["close"]

    # Split data into training (80%) and testing (20%) sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define hyperparameter grid for model tuning
    param_grid = {
        "max_iter": [75, 100],  # Number of boosting iterations
        "max_depth": [3, 4],  # Maximum depth of trees
        "learning_rate": [0.01, 0.001],  # Step size shrinkage
        "min_samples_leaf": [30, 60],  # Minimum number of samples per leaf
        "l2_regularization": [0.1, 0.5]  # L2 regularization strength
    }

    # Perform grid search to find the best model parameters
    model = GridSearchCV(HistGradientBoostingRegressor(random_state=42), param_grid,
                         cv=3, scoring="neg_mean_squared_error", n_jobs=-1)
    
    # Train the model on the training set
    model.fit(X_train, y_train)

    # Save the best-performing model to a file
    joblib.dump(model.best_estimator_, MODEL_FILE)

    # Generate predictions on the test set
    y_test_pred = model.best_estimator_.predict(X_test)

    # Compute model evaluation metrics
    metrics_df = pd.DataFrame({
        "metric": ["R²", "MSE", "MAE"],
        "value": [r2_score(y_test, y_test_pred), mean_squared_error(y_test, y_test_pred), mean_absolute_error(y_test, y_test_pred)]
    })

    # Store the computed metrics in the PostgreSQL database
    metrics_df.to_sql("model_metrics", engine, if_exists="replace", index=False)

    print("✅ Model trained and metrics stored in PostgreSQL")

if __name__ == "__main__":
    train_model()
