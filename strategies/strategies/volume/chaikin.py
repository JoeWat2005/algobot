from strategies.base import Strategy
import pandas as pd

class ChaikinMoneyFlowStrategy(Strategy):
    def __init__(self, period=20):
        self.period = period

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        # Flatten columns if MultiIndex
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        print("\n[ChaikinMoneyFlowStrategy] Input index:", type(df.index))
        print("[ChaikinMoneyFlowStrategy] Input head:")
        print(df.head(3))

        # Prevent division by zero in range
        range_ = df['High'] - df['Low']
        range_ = range_.replace(0, 1e-10)

        # Money Flow Multiplier and Volume
        mf_multiplier = ((df['Close'] - df['Low']) - (df['High'] - df['Close'])) / range_
        mf_volume = mf_multiplier * df['Volume']

        # CMF Calculation
        cmf = mf_volume.rolling(self.period).sum() / df['Volume'].rolling(self.period).sum()
        df['cmf'] = cmf

        # Generate signals
        df['signal'] = 0
        df.loc[cmf > 0, 'signal'] = 1
        df.loc[cmf < 0, 'signal'] = -1

        # Debug output
        print("[ChaikinMoneyFlowStrategy] signal counts:\n", df['signal'].value_counts())

        return df

