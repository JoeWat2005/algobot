from strategies.base import Strategy
import pandas as pd

class MomentumStrategy(Strategy):
    def __init__(self, window=10, threshold=0.02):
        self.window = window
        self.threshold = threshold

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        df['roc'] = df['Close'].pct_change(self.window)
        df['signal'] = 0
        df.loc[df['roc'] > self.threshold, 'signal'] = 1
        df.loc[df['roc'] < -self.threshold, 'signal'] = -1
        return df
