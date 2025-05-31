from strategies.base import Strategy
import pandas as pd

class ATRStrategy(Strategy):
    def __init__(self, period=14, multiplier=1.5):
        self.period = period
        self.multiplier = multiplier

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        # Flatten columns if MultiIndex
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        print("\n[ATRStrategy] Input index:", type(df.index))
        print("[ATRStrategy] Input head:")
        print(df.head(3))

        # True Range components
        tr1 = df['High'] - df['Low']
        tr2 = (df['High'] - df['Close'].shift()).abs()
        tr3 = (df['Low'] - df['Close'].shift()).abs()

        # Combine into a Series (row-wise max of three columns)
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

        # ATR as rolling mean of True Range
        atr = tr.rolling(self.period).mean()

        # Ensure all values are Series with aligned indexes
        close = df['Close']
        prev_close = close.shift(1)

        # Align explicitly just to be safe
        atr, _ = atr.align(close, axis=0)
        prev_close, _ = prev_close.align(close, axis=0)

        # Generate signals
        df['atr'] = atr
        df['signal'] = 0
        df.loc[close > (prev_close + self.multiplier * atr), 'signal'] = 1
        df.loc[close < (prev_close - self.multiplier * atr), 'signal'] = -1

        print("[ATRStrategy] signal counts:\n", df['signal'].value_counts())

        return df

