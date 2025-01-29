 # AMZN Stock Forecasting with Airflow and HGBR

## 📌 Project Overview
This project automates stock price prediction for **Amazon (AMZN)** using **Apache Airflow**, **Docker**, and **HistGradientBoostingRegressor (HGBR)**. The pipeline:
- Retrieves stock data from the **Alpha Vantage API**.
- Computes **technical indicators** (SMA, RSI, volatility, OBV).
- Trains an ML model with **HGBR and hyperparameter tuning**.
- Predicts stock prices and evaluates model performance.
- Generates a **visual comparison** of actual vs. predicted prices with key metrics (**R², MSE, MAE**).

The workflow is fully **containerized using Docker**, ensuring **scalability, reproducibility, and easy deployment**.

---

## 📌 Data Source: Alpha Vantage API
The pipeline fetches **daily stock price data** from [Alpha Vantage API](https://www.alphavantage.co/documentation/) using the `TIME_SERIES_DAILY` function.

### **Example API Request**
```bash
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AMZN&apikey=YOUR_API_KEY&outputsize=full&datatype=json
```
**Extracted Features:**
- **Market data:** `open`, `high`, `low`, `close`, `volume`
- **Computed indicators:** `SMA (7 & 14 days)`, `volatility`, `RSI`, `OBV`

To use the API, obtain a **free API key** from [Alpha Vantage](https://www.alphavantage.co/support/#api-key).

---

## 📌 Project Structure
```
├── dags/                          # Airflow DAGs
│   ├── amzn_forecast_pipeline.py  # DAG definition
├── data/                          # Data storage
│   ├── extracted_data.csv         # Raw stock data
│   ├── processed_data.csv         # Preprocessed dataset
│   ├── predictions.csv            # Stock price predictions
│   ├── model_metrics.csv          # Performance metrics (R², MSE, MAE)
│   ├── plots/                     # Visualization output
│   │   ├── amzn_predictions.png   # Actual vs. predicted prices
├── models/                        # Trained ML models
│   ├── amzn_model.pkl             # Saved model
├── scripts/                       # Python scripts
│   ├── extract_data.py            # Fetches AMZN stock data
│   ├── preprocess_data.py         # Processes stock data
│   ├── train_model.py             # Trains HGBR model
│   ├── predict.py                 # Generates predictions
│   ├── visualize_predictions.py   # Plots results
├── docker-compose.yaml            # Docker setup
├── requirements.txt               # Dependencies
└── README.md                      # Documentation
```

---

## 📌 Pipeline Workflow
This **end-to-end ML pipeline** runs in **Apache Airflow**:

1️⃣ **Extract Data** → Fetch AMZN stock data (`extract_data.py`).  
2️⃣ **Preprocess Data** → Clean data, compute indicators (`preprocess_data.py`).  
3️⃣ **Train Model** → Train HGBR with hyperparameter tuning (`train_model.py`).  
4️⃣ **Make Predictions** → Predict stock prices (`predict.py`).  
5️⃣ **Visualize Results** → Generate plots and model evaluation (`visualize_predictions.py`).  

Airflow DAG execution order:
```
extract_data >> preprocess_data >> train_model >> predict >> visualize_predictions
```

---

## 📌 Setup and Execution Guide

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/FranRguezCer/amzn-stocks-predictions-airflow.git
cd amzn-stock-forecast
```

### 2️⃣ Set Up Docker and Airflow
Ensure **Docker** and **Docker Compose** are installed. Then, start the Airflow containers:
```bash
docker-compose up -d  # Start Airflow services
```

### 3️⃣ Access Airflow Web UI
Once running, open:
```
http://localhost:8080
```
- **DAG Name:** `amzn_forecast_pipeline`
- Enable the DAG and trigger a **manual run**.

### 4️⃣ View Results
Once the DAG completes:
- **Predictions:** `data/predictions.csv`
- **Model Metrics:** `data/model_metrics.csv`
- **Visualization:** `data/plots/amzn_predictions.png`

---

## 📌 Model Performance Evaluation
Evaluated on **20% test data**, key metrics include:
- **R² Score**: Accuracy of predictions.
- **MSE (Mean Squared Error)**: Error magnitude.
- **MAE (Mean Absolute Error)**: Average deviation.

Metrics are **displayed on the visualization**, centered at the top.

---

## 📌 Dependency Management with Docker
You **do not need to install dependencies manually**. Docker Compose installs them inside the container:

```yaml
airflow_worker:
  container_name: airflow_worker
  <<: *airflow-common
  command: celery worker
  restart: always
  depends_on:
    airflow_init:
      condition: service_completed_successfully
  entrypoint: >
    sh -c "pip install -r /opt/airflow/requirements.txt && exec airflow celery worker"
```

### ❌ No Need for Manual Installation
Do **not** run:
```bash
pip install -r requirements.txt
```
This is already handled inside the Docker container.

### ⚠️ When to Install Manually?
Only if:
- Running scripts **outside Docker**.
- Adding a new library **without restarting containers**.

Manual install:
```bash
pip install -r requirements.txt
```

### 🚀 Conclusion
With Docker Compose, dependencies are fully managed **inside the container**. To start the project:
```bash
docker-compose up -d
```

🔹 **Your Airflow pipeline is fully functional inside the Docker environment!** 🚀

---

## 📌 Example Visualization Output
The pipeline generates a **comparison plot**:

![AMZN Stock Prediction](data/plots/amzn_predictions.png)

Metrics **(R², MSE, MAE)** are displayed at the top.

---

## 📌 Future Improvements
🚀 **Next steps:**
- Optimize hyperparameters using **Bayesian Search**.
- Add more **market indicators** (e.g., Bollinger Bands).
- Implement **LSTM/Transformer models** for better forecasting.

---

## 📌 License
This project is open-source under the **MIT License**.

---

**Author:** Francisco José Rodríguez Cerezo  
📧 Contact: [portfolio.fjrguezcer@gmail.com](mailto:portfolio.fjrguezcer@gmail.com)  
👉 GitHub: [FranRguezCer](https://github.com/FranRguezCer/)
