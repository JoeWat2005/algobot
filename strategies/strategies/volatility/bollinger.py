from strategies.base import Strategy
import pandas as pd

class BollingerBandsStrategy(Strategy):
    def __init__(self, window=20, num_std=2):
        self.window = window
        self.num_std = num_std

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        df['ma'] = df['Close'].rolling(self.window).mean()
        df['std'] = df['Close'].rolling(self.window).std()
        df['upper_band'] = df['ma'] + self.num_std * df['std']
        df['lower_band'] = df['ma'] - self.num_std * df['std']
        df['signal'] = 0
        df.loc[df['Close'] < df['lower_band'], 'signal'] = 1
        df.loc[df['Close'] > df['upper_band'], 'signal'] = -1
        return df
