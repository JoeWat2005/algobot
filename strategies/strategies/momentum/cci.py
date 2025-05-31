from strategies.base import Strategy
import pandas as pd

class CCIStrategy(Strategy):
    def __init__(self, period=20, threshold=100):
        self.period = period
        self.threshold = threshold

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        # Flatten MultiIndex columns if necessary
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        print("\n[CCIStrategy] Input index:", type(df.index))
        print("[CCIStrategy] Input head:")
        print(df.head(3))

        # Typical price
        tp = (df['High'] + df['Low'] + df['Close']) / 3

        # Rolling mean and mean deviation
        ma = tp.rolling(self.period).mean()
        md = tp.rolling(self.period).apply(lambda x: abs(x - x.mean()).mean(), raw=False)

        # CCI calculation
        cci = (tp - ma) / (0.015 * md)
        df['cci'] = cci

        # Generate signals
        df['signal'] = 0
        df.loc[cci > self.threshold, 'signal'] = -1
        df.loc[cci < -self.threshold, 'signal'] = 1

        # Debug output
        print("[CCIStrategy] signal counts:\n", df['signal'].value_counts())

        return df
