from strategies.base import Strategy
import pandas as pd

class QuantileBandsStrategy(Strategy):
    def __init__(self, window=20, lower_q=0.1, upper_q=0.9):
        self.window = window
        self.lower_q = lower_q
        self.upper_q = upper_q

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        # Flatten columns if MultiIndex
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        print("\n[QuantileBandsStrategy] Input index:", type(df.index))
        print("[QuantileBandsStrategy] Input head:")
        print(df.head(3))

        # Rolling quantiles
        rolling_window = df['Close'].rolling(self.window)
        lower_q = rolling_window.quantile(self.lower_q)
        upper_q = rolling_window.quantile(self.upper_q)

        lower_q, close = lower_q.align(df['Close'], axis=0)
        upper_q, _ = upper_q.align(df['Close'], axis=0)

        df['signal'] = 0
        df.loc[close < lower_q, 'signal'] = 1
        df.loc[close > upper_q, 'signal'] = -1
        df['lower_quantile'] = lower_q
        df['upper_quantile'] = upper_q

        print("[QuantileBandsStrategy] signal counts:\n", df['signal'].value_counts())

        return df
