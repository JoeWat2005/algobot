from strategies.base import Strategy
import pandas as pd

class MLStubStrategy(Strategy):
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        # Flatten MultiIndex columns if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        print("\n[MLStubStrategy] Input index:", type(df.index))
        print("[MLStubStrategy] Input head:")
        print(df.head(3))

        # Placeholder signal logic
        df['signal'] = 0

        print("[MLStubStrategy] signal counts:\n", df['signal'].value_counts())

        return df
