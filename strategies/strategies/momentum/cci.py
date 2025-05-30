from strategies.base import Strategy
import pandas as pd

class CCIStrategy(Strategy):
    def __init__(self, period=20, threshold=100):
        self.period = period
        self.threshold = threshold

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        tp = (df['High'] + df['Low'] + df['Close']) / 3
        ma = tp.rolling(self.period).mean()
        md = tp.rolling(self.period).apply(lambda x: abs(x - x.mean()).mean())
        df['cci'] = (tp - ma) / (0.015 * md)
        df['signal'] = 0
        df.loc[df['cci'] > self.threshold, 'signal'] = -1
        df.loc[df['cci'] < -self.threshold, 'signal'] = 1
        return df