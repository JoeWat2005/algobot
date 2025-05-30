from strategies.base import Strategy
import pandas as pd

class ZScoreStrategy(Strategy):
    def __init__(self, period=20, threshold=1.5):
        self.period = period
        self.threshold = threshold

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        df['mean'] = df['Close'].rolling(self.period).mean()
        df['std'] = df['Close'].rolling(self.period).std()
        df['zscore'] = (df['Close'] - df['mean']) / df['std']
        df['signal'] = 0
        df.loc[df['zscore'] > self.threshold, 'signal'] = -1
        df.loc[df['zscore'] < -self.threshold, 'signal'] = 1
        return df