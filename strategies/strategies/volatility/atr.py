from strategies.base import Strategy
import pandas as pd

class ATRStrategy(Strategy):
    def __init__(self, period=14, multiplier=1.5):
        self.period = period
        self.multiplier = multiplier

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        tr1 = df['High'] - df['Low']
        tr2 = abs(df['High'] - df['Close'].shift())
        tr3 = abs(df['Low'] - df['Close'].shift())
        df['tr'] = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        df['atr'] = df['tr'].rolling(self.period).mean()
        df['signal'] = 0
        df.loc[df['Close'] > df['Close'].shift(1) + self.multiplier * df['atr'], 'signal'] = 1
        df.loc[df['Close'] < df['Close'].shift(1) - self.multiplier * df['atr'], 'signal'] = -1
        return df
