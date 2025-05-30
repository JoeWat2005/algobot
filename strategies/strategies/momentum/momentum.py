from strategies.base import Strategy
import pandas as pd

class MomentumStrategy(Strategy):
    def __init__(self, period=10):
        self.period = period

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        df['momentum'] = df['Close'] - df['Close'].shift(self.period)
        df['signal'] = 0
        df.loc[df['momentum'] > 0, 'signal'] = 1
        df.loc[df['momentum'] < 0, 'signal'] = -1
        return df