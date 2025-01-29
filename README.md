# AMZN Stock Forecasting with Airflow and HGBR

## 📌 Project Overview
This project builds an **automated machine learning pipeline** for predicting **Amazon (AMZN) stock prices** using **Apache Airflow** and **HistGradientBoostingRegressor (HGBR)**. The pipeline:
- Extracts **AMZN** stock market data from the **Alpha Vantage API**.
- Processes the data and computes **technical indicators** (SMA, RSI, volatility, OBV).
- Trains an ML model using **HGBR** with **hyperparameter tuning**.
- Generates stock price **predictions**.
- Visualizes **actual vs predicted prices**, including model **test metrics (R², MSE, MAE)**.

The workflow is **containerized with Docker**, ensuring **reproducibility** and **easy deployment**.

---

## 📌 Data Source: Alpha Vantage API
We retrieve **daily stock price data** from the [Alpha Vantage API](https://www.alphavantage.co/documentation/), using the `TIME_SERIES_DAILY` function.

### **Example API Request**
```bash
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AMZN&apikey=YOUR_API_KEY&outputsize=full&datatype=json
```
**Extracted Features:**
- **Raw data:** `open`, `high`, `low`, `close`, `volume`
- **Computed indicators:** `SMA (7 & 14 days)`, `volatility`, `RSI`, `OBV`

To use the API, get a **free API key** from [Alpha Vantage](https://www.alphavantage.co/support/#api-key).

---

## 📌 Project Structure
```
├── dags/                                 # Airflow DAGs folder
│   ├── amzn_forecast_pipeline.py         # DAG definition
├── data/                                 # Data storage
│   ├── extracted_data.csv                # Raw stock data from API
│   ├── processed_data.csv                # Preprocessed dataset with indicators
│   ├── predictions.csv                   # Model predictions
│   ├── model_metrics.csv                 # Model performance metrics (Test R², MSE, MAE)
│   ├── plots/                            # Visualization output
│   │   ├── amzn_predictions.png          # Plot of actual vs predicted prices
├── models/                               # Trained ML models
│   ├── amzn_model.pkl                    # Saved model
├── scripts/                              # Python scripts for each pipeline step
│   ├── extract_data.py                   # Fetches AMZN stock data from API
│   ├── preprocess_data.py                # Processes stock data & computes indicators
│   ├── train_model.py                    # Trains HGBR model with GridSearchCV
│   ├── predict.py                        # Generates AMZN stock price predictions
│   ├── visualize_predictions.py          # Creates comparison plot with test metrics
├── docker-compose.yaml                   # Docker configuration for Airflow
├── requirements.txt                      # Python dependencies
└── README.md                             # Project documentation
```

---

## 📌 Pipeline Workflow
This **end-to-end forecasting pipeline** is orchestrated in **Apache Airflow**:

1️⃣ **Extract Data** → Fetch AMZN stock data from Alpha Vantage API (`extract_data.py`).  
2️⃣ **Preprocess Data** → Clean data, generate technical indicators (`preprocess_data.py`).  
3️⃣ **Train Model** → Train HGBR model with hyperparameter tuning (`train_model.py`).  
4️⃣ **Make Predictions** → Predict stock closing prices (`predict.py`).  
5️⃣ **Visualize Results** → Generate a plot with actual vs predicted values (`visualize_predictions.py`).  

Airflow DAG Execution Order:
```
extract_data >> preprocess_data >> train_model >> predict >> visualize_predictions
```

---

## 📌 Setup and Execution Guide

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/FranRguezCer/amzn-stock-forecast.git
cd amzn-stock-forecast
```

### 2️⃣ Set Up Docker and Airflow
Ensure **Docker** and **Docker Compose** are installed. Then, start the Airflow containers:
```bash
docker-compose up -d  # Start Airflow services
```

### 3️⃣ Access Airflow Web UI
Once containers are running, access the Airflow UI:
```
http://localhost:8080
```
- **DAG Name:** `amzn_forecast_pipeline`
- Enable the DAG and trigger a **manual run**.

### 4️⃣ View Results
Once the DAG completes:
- **Check Predictions:** `data/predictions.csv`
- **Check Model Metrics:** `data/model_metrics.csv`
- **View Visualization:** `data/plots/amzn_predictions.png`

---

## 📌 Model Performance Evaluation
The model is evaluated on **20% test data**, with the following metrics:

💊 **Metrics Stored in `data/model_metrics.csv`**  
- **R² Score (R²)**: Measures model accuracy.
- **Mean Squared Error (MSE)**: Measures prediction error.
- **Mean Absolute Error (MAE)**: Measures average deviation from actual price.

These metrics are **displayed on the final visualization**, centered at the top of the plot.

---

## 📌 Dependencies
Ensure dependencies are installed:
```bash
pip install -r requirements.txt
```
Required libraries:
```plaintext
apache-airflow
apache-airflow-providers-docker
pandas
numpy
scikit-learn
matplotlib
requests
```

---

## 📌 Example Visualization Output
Once the pipeline runs successfully, it generates the following **comparison plot**:

![AMZN Stock Prediction](data/plots/amzn_predictions.png)

The plot **includes model performance metrics (R², MSE, MAE) at the top**.

---

## 📌 Future Improvements
🚀 **Enhancements for future versions:**
- Add **hyperparameter optimization** using Bayesian Search.
- Incorporate **additional market indicators** like Bollinger Bands.
- Implement **deep learning models (LSTM, Transformer)** for improved forecasting.

---

## 📌 License
This project is open-source and available under the **MIT License**.

---

**Author:** Francisco José Rodríguez Cerezo  
📧 Contact: [portfolio.fjrguezcer@gmail.com](mailto:portfolio.fjrguezcer@gmail.com)  
👉 GitHub: [FranRguezCer](https://github.com/FranRguezCer/)