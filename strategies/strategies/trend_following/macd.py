from strategies.base import Strategy
import pandas as pd

class MACDStrategy(Strategy):
    def __init__(self, fast=12, slow=26, signal=9):
        self.fast = fast
        self.slow = slow
        self.signal = signal

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        # Flatten MultiIndex columns if necessary
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        print("\n[MACDStrategy] Input index:", type(df.index))
        print("[MACDStrategy] Input head:")
        print(df.head(3))

        # Calculate MACD components
        df['ema_fast'] = df['Close'].ewm(span=self.fast, adjust=False).mean()
        df['ema_slow'] = df['Close'].ewm(span=self.slow, adjust=False).mean()
        df['macd'] = df['ema_fast'] - df['ema_slow']
        df['macd_signal'] = df['macd'].ewm(span=self.signal, adjust=False).mean()

        # Generate signals
        df['signal'] = 0
        df.loc[df['macd'] > df['macd_signal'], 'signal'] = 1
        df.loc[df['macd'] < df['macd_signal'], 'signal'] = -1

        # Debug output
        print("[MACDStrategy] signal counts:\n", df['signal'].value_counts())

        return df
