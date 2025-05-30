from strategies.base import Strategy
import pandas as pd

class QuantileBandsStrategy(Strategy):
    def __init__(self, window=20, lower_q=0.1, upper_q=0.9):
        self.window = window
        self.lower_q = lower_q
        self.upper_q = upper_q

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        df['lower_quantile'] = df['Close'].rolling(self.window).quantile(self.lower_q)
        df['upper_quantile'] = df['Close'].rolling(self.window).quantile(self.upper_q)
        df['signal'] = 0

        df.loc[df['Close'] < df['lower_quantile'], 'signal'] = 1
        df.loc[df['Close'] > df['upper_quantile'], 'signal'] = -1
        return df
