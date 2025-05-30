from strategies.base import Strategy
import pandas as pd
import numpy as np

class ADXStrategy(Strategy):
    def __init__(self, period=14, threshold=25):
        self.period = period
        self.threshold = threshold

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        high_diff = df['High'].diff()
        low_diff = df['Low'].diff()

        plus_dm = np.where((high_diff > low_diff) & (high_diff > 0), high_diff, 0)
        minus_dm = np.where((low_diff > high_diff) & (low_diff > 0), low_diff, 0)

        tr1 = df['High'] - df['Low']
        tr2 = abs(df['High'] - df['Close'].shift())
        tr3 = abs(df['Low'] - df['Close'].shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

        atr = tr.rolling(self.period).mean()
        plus_di = 100 * (pd.Series(plus_dm, index=df.index).rolling(self.period).sum() / atr)
        minus_di = 100 * (pd.Series(minus_dm, index=df.index).rolling(self.period).sum() / atr)
        dx = (abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
        adx = dx.rolling(self.period).mean()

        df['adx'] = adx
        df['signal'] = 0
        df.loc[df['adx'] > self.threshold, 'signal'] = 1
        df.loc[df['adx'] < self.threshold, 'signal'] = -1
        return df
