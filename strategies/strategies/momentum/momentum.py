from strategies.base import Strategy
import pandas as pd

class MomentumStrategy(Strategy):
    def __init__(self, period=10):
        self.period = period

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        # Flatten MultiIndex columns if necessary
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        print("\n[MomentumStrategy] Input index:", type(df.index))
        print("[MomentumStrategy] Input head:")
        print(df.head(3))

        # Calculate momentum
        df['momentum'] = df['Close'] - df['Close'].shift(self.period)

        # Generate signals
        df['signal'] = 0
        df.loc[df['momentum'] > 0, 'signal'] = 1
        df.loc[df['momentum'] < 0, 'signal'] = -1

        # Debug output
        print("[MomentumStrategy] signal counts:\n", df['signal'].value_counts())

        return df
