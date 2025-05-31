from strategies.base import Strategy
import pandas as pd
import numpy as np

class ParabolicSARStrategy(Strategy):
    def __init__(self, af_step=0.02, af_max=0.2):
        self.af_step = af_step
        self.af_max = af_max

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        # Flatten columns if MultiIndex
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        print("\n[ParabolicSARStrategy] Input index:", type(df.index))
        print("[ParabolicSARStrategy] Input head:")
        print(df.head(3))

        psar = df['Close'].copy()
        bull = True
        af = self.af_step
        ep = df['Low'].iloc[0]
        hp = df['High'].iloc[0]

        for i in range(1, len(df)):
            prev_psar = psar.iloc[i - 1]

            if bull:
                psar_val = prev_psar + af * (hp - prev_psar)
                if df['Low'].iloc[i] < psar_val:
                    # Trend reversal to bear
                    bull = False
                    psar_val = hp
                    af = self.af_step
                    ep = df['Low'].iloc[i]
                else:
                    if df['High'].iloc[i] > hp:
                        hp = df['High'].iloc[i]
                        af = min(af + self.af_step, self.af_max)
            else:
                psar_val = prev_psar + af * (ep - prev_psar)
                if df['High'].iloc[i] > psar_val:
                    # Trend reversal to bull
                    bull = True
                    psar_val = ep
                    af = self.af_step
                    hp = df['High'].iloc[i]
                else:
                    if df['Low'].iloc[i] < ep:
                        ep = df['Low'].iloc[i]
                        af = min(af + self.af_step, self.af_max)

            psar.iloc[i] = psar_val

        df['psar'] = psar
        df['signal'] = 0
        df.loc[df['Close'] > df['psar'], 'signal'] = 1
        df.loc[df['Close'] < df['psar'], 'signal'] = -1

        print("[ParabolicSARStrategy] signal counts:\n", df['signal'].value_counts())

        return df
