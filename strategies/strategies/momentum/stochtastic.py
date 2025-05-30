from strategies.base import Strategy
import pandas as pd

class StochasticOscillatorStrategy(Strategy):
    def __init__(self, k_period=14, d_period=3):
        self.k_period = k_period
        self.d_period = d_period

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        low_min = df['Low'].rolling(window=self.k_period).min()
        high_max = df['High'].rolling(window=self.k_period).max()
        df['%K'] = 100 * ((df['Close'] - low_min) / (high_max - low_min))
        df['%D'] = df['%K'].rolling(window=self.d_period).mean()
        df['signal'] = 0
        df.loc[df['%K'] > df['%D'], 'signal'] = 1
        df.loc[df['%K'] < df['%D'], 'signal'] = -1
        return df