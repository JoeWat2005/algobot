from strategies.base import Strategy
import pandas as pd

class StdDevStrategy(Strategy):
    def __init__(self, period=20, threshold=2):
        self.period = period
        self.threshold = threshold

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        # Flatten MultiIndex columns if necessary
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        print("\n[StdDevStrategy] Input index:", type(df.index))
        print("[StdDevStrategy] Input head:")
        print(df.head(3))

        # Calculate rolling mean and standard deviation
        mean = df['Close'].rolling(self.period).mean()
        std = df['Close'].rolling(self.period).std()

        # Compute z-score
        zscore = (df['Close'] - mean) / std
        if isinstance(zscore, pd.DataFrame):
            print("[StdDevStrategy] zscore is a DataFrame — flattening it.")
            zscore = zscore.iloc[:, 0]

        # Assign calculated columns
        df['mean'] = mean
        df['std'] = std
        df['zscore'] = zscore

        # Generate signals
        df['signal'] = 0
        df.loc[zscore > self.threshold, 'signal'] = -1
        df.loc[zscore < -self.threshold, 'signal'] = 1

        print("[StdDevStrategy] signal counts:\n", df['signal'].value_counts())

        return df
