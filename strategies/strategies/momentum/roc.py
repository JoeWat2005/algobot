from strategies.base import Strategy
import pandas as pd

class ROCStrategy(Strategy):
    def __init__(self, period=12):
        self.period = period

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        df['roc'] = df['Close'].pct_change(periods=self.period) * 100
        df['signal'] = 0
        df.loc[df['roc'] > 0, 'signal'] = 1
        df.loc[df['roc'] < 0, 'signal'] = -1
        return df