from strategies.base import Strategy
import pandas as pd

class ROCStrategy(Strategy):
    def __init__(self, period=12):
        self.period = period

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        # Flatten MultiIndex columns if needed
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        print("\n[ROCStrategy] Input index:", type(df.index))
        print("[ROCStrategy] Input head:")
        print(df.head(3))

        # Calculate Rate of Change
        df['roc'] = df['Close'].pct_change(periods=self.period) * 100

        # Generate signals
        df['signal'] = 0
        df.loc[df['roc'] > 0, 'signal'] = 1
        df.loc[df['roc'] < 0, 'signal'] = -1

        # Debugging output
        print("[ROCStrategy] signal counts:\n", df['signal'].value_counts())

        return df
