import yfinance as yf
import pandas as pd

class Market:
    def get_data(self, symbol, start, end):
        df = yf.download(symbol, start, end)
        df.dropna(inplace = True)
        return df
    