## Overview
This project processes high-frequency tick data from Binance Futures and aggregates it into 1-minute OHLCV (Open, High, Low, Close, Volume) candles.

## Features
* **Ingestion:** Reads raw tick data from NDJSON format.
* **Data Cleaning:** Filters out anomalies (zero-price ticks, bad payloads) to ensure data integrity.
* **Aggregation:** Resamples tick-by-tick data into 1-minute intervals using Pandas.
* **Output:** Generates clean CSV files ready for backtesting or analysis.

## Project Structure
* `process_data.py`: Main script for parsing and aggregation.
* `ticks_*.ndjson`: Raw input data (collected via WebSocket).
* `*_aggregated.csv`: Final output files.

## Setup & Usage
1.  **Install Dependencies:**
    ```bash
    pip install pandas
    ```

2.  **Run the Aggregator:**
    Ensure your input NDJSON file is in the root directory and update the filename in the script if necessary.
    ```bash
    python process_data.py
    ```

3.  **Output:**
    The script will generate `BTCUSDT_aggregated.csv` and `ETHUSDT_aggregated.csv`.

## logic
The aggregator uses a robust cleaning logic to handle potential WebSocket errors:
```python
# Remove rows where price is 0 or negative
df = df[df['price'] > 0]
