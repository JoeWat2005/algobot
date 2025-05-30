import json
import yfinance as yf

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

    def get_all_data(self):
        data = {}
        for ticker in self.tickers:
            print(f"Loading data for {ticker}...")
            df = yf.download(ticker, start=self.start_date, end=self.end_date)
            df.dropna(inplace=True)
            data[ticker] = df
        return data
            