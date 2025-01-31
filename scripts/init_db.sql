CREATE TABLE IF NOT EXISTS stock_data (
    date DATE PRIMARY KEY,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    volume FLOAT
);

CREATE TABLE IF NOT EXISTS processed_data (
    date DATE PRIMARY KEY,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    volume FLOAT,
    weekday INT,
    month INT,
    year INT,
    return FLOAT,
    volatility FLOAT,
    sma_7 FLOAT,
    sma_14 FLOAT,
    rsi FLOAT,
    obv FLOAT
);

CREATE TABLE IF NOT EXISTS predictions (
    date DATE PRIMARY KEY,
    close FLOAT,
    predicted_close FLOAT
);

CREATE TABLE IF NOT EXISTS model_metrics (
    metric VARCHAR(50) PRIMARY KEY,
    value FLOAT
);
