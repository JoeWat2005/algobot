from strategies.base import Strategy
import pandas as pd

class AccumulationDistributionStrategy(Strategy):
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        # Flatten columns if MultiIndex
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        print("\n[AccumulationDistributionStrategy] Input index:", type(df.index))
        print("[AccumulationDistributionStrategy] Input head:")
        print(df.head(3))

        # Calculate range, CLV, ADL
        range_ = df['High'] - df['Low']
        range_ = range_.replace(0, 1e-10)  # Avoid division by zero

        clv = ((df['Close'] - df['Low']) - (df['High'] - df['Close'])) / range_
        adl = (clv * df['Volume']).cumsum()

        # EMA of ADL
        adl_ema = adl.ewm(span=20).mean()

        # Add to DataFrame
        df['adl'] = adl
        df['adl_ema'] = adl_ema

        # Generate signals
        df['signal'] = 0
        df.loc[adl > adl_ema, 'signal'] = 1
        df.loc[adl < adl_ema, 'signal'] = -1

        # Debug output
        print("[AccumulationDistributionStrategy] signal counts:\n", df['signal'].value_counts())

        return df
