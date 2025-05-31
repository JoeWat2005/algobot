from strategies.base import Strategy
import pandas as pd

class MovingAverageCrossover(Strategy):
    def __init__(self, short_window=50, long_window=200):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        # Flatten MultiIndex columns if necessary
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        print("\n[MovingAverageCrossover] Input index:", type(df.index))
        print("[MovingAverageCrossover] Input head:")
        print(df.head(3))

        # Calculate moving averages
        short_ma = df['Close'].rolling(window=self.short_window).mean()
        long_ma = df['Close'].rolling(window=self.long_window).mean()

        df['short_ma'] = short_ma
        df['long_ma'] = long_ma

        # Generate signals
        df['signal'] = 0
        df.loc[short_ma > long_ma, 'signal'] = 1
        df.loc[short_ma < long_ma, 'signal'] = -1

        # Debug output
        print("[MovingAverageCrossover] signal counts:\n", df['signal'].value_counts())

        return df
