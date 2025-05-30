import json
import yfinance as yf
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

class Market:
    def __init__(self, config_path="data/tickers.json"):
        self.config_path = config_path
        self.tickers = []
        self.start_date = ""
        self.end_date = ""
        self._load_config()

    def _load_config(self):
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        self.tickers = config.get("tickers", [])
        self.start_date = config.get("start_date", "2020-01-01")
        self.end_date = config.get("end_date", "2024-01-01")

    def _download_single_ticker(self, ticker):
        try:
            print(f"Downloading {ticker}...")
            df = yf.download(ticker, start=self.start_date, end=self.end_date, auto_adjust=True, progress=False)
            df.dropna(inplace=True)
            return ticker, df
        except Exception as e:
            print(f"Failed to download {ticker}: {e}")
            return ticker, None

    def get_all_data(self, max_workers=64):
        data = {}
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self._download_single_ticker, ticker) for ticker in self.tickers]
            for future in as_completed(futures):
                ticker, df = future.result()
                if df is not None:
                    data[ticker] = df
        return data

            