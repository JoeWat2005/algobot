from strategies.base import Strategy
import pandas as pd

class KeltnerChannelStrategy(Strategy):
    def __init__(self, period=20, atr_multiplier=2):
        self.period = period
        self.atr_multiplier = atr_multiplier

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        # Flatten columns if MultiIndex
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        print("\n[KeltnerChannelStrategy] Input index:", type(df.index))
        print("[KeltnerChannelStrategy] Input head:")
        print(df.head(3))

        # Typical price
        typical_price = (df['High'] + df['Low'] + df['Close']) / 3
        ma = typical_price.rolling(self.period).mean()

        # True Range components
        tr1 = df['High'] - df['Low']
        tr2 = (df['High'] - df['Close'].shift()).abs()
        tr3 = (df['Low'] - df['Close'].shift()).abs()
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(self.period).mean()

        # Align everything
        close, ma = df['Close'].align(ma, axis=0)
        _, atr = close.align(atr, axis=0)

        # Bands
        upper_band = ma + self.atr_multiplier * atr
        lower_band = ma - self.atr_multiplier * atr

        # Assign bands
        df['ma'] = ma
        df['atr'] = atr
        df['upper_band'] = upper_band
        df['lower_band'] = lower_band

        # Signal generation
        df['signal'] = 0
        df.loc[close > upper_band, 'signal'] = -1
        df.loc[close < lower_band, 'signal'] = 1

        print("[KeltnerChannelStrategy] signal counts:\n", df['signal'].value_counts())

        return df

