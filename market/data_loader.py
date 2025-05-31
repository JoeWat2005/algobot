import json
import yfinance as yf
import pandas as pd
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

class Market:
    def __init__(self, config_path="data/tickers.json", max_retries=5, retry_delay=2):
        self.config_path = config_path
        self.tickers = []
        self.start_date = ""
        self.end_date = ""
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self._load_config()

    def _load_config(self):
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        self.tickers = config.get("tickers", [])
        self.start_date = config.get("start_date", "2020-01-01")
        self.end_date = config.get("end_date", "2024-01-01")

    def _download_single_ticker(self, ticker):
        for attempt in range(1, self.max_retries + 1):
            try:
                print(f"[{ticker}] Attempt {attempt}/{self.max_retries}...")
                df = yf.download(ticker, start=self.start_date, end=self.end_date, auto_adjust=True, progress=False)
                df.dropna(inplace=True)
                if not df.empty:
                    print(f"[{ticker}] Download successful.")
                    return ticker, df
                else:
                    print(f"[{ticker}] Empty DataFrame received.")
            except Exception as e:
                print(f"[{ticker}] Attempt {attempt} failed: {e}")
            time.sleep(self.retry_delay)
        print(f"[{ticker}] All {self.max_retries} attempts failed.")
        return ticker, None

    def get_all_data(self, max_workers=None):
        if max_workers is None:
            max_workers = min(32, (os.cpu_count() or 1) + 4)

        print(f"Using max_workers = {max_workers} for downloading...")

        data = {}
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self._download_single_ticker, ticker) for ticker in self.tickers]
            for future in as_completed(futures):
                ticker, df = future.result()
                if df is not None:
                    data[ticker] = df
        return data

            