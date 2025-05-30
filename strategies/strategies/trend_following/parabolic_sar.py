from strategies.base import Strategy
import pandas as pd
import numpy as np

class ParabolicSARStrategy(Strategy):
    def __init__(self, af_step=0.02, af_max=0.2):
        self.af_step = af_step
        self.af_max = af_max

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        psar = df['Close'].copy()
        bull = True
        af = self.af_step
        ep = df['Low'].iloc[0]
        hp = df['High'].iloc[0]

        for i in range(1, len(df)):
            if bull:
                psar.iloc[i] = psar.iloc[i - 1] + af * (hp - psar.iloc[i - 1])
                if df['Low'].iloc[i] < psar.iloc[i]:
                    bull = False
                    psar.iloc[i] = hp
                    af = self.af_step
                    ep = df['Low'].iloc[i]
            else:
                psar.iloc[i] = psar.iloc[i - 1] + af * (ep - psar.iloc[i - 1])
                if df['High'].iloc[i] > psar.iloc[i]:
                    bull = True
                    psar.iloc[i] = ep
                    af = self.af_step
                    hp = df['High'].iloc[i]

            if bull:
                if df['High'].iloc[i] > hp:
                    hp = df['High'].iloc[i]
                    af = min(af + self.af_step, self.af_max)
            else:
                if df['Low'].iloc[i] < ep:
                    ep = df['Low'].iloc[i]
                    af = min(af + self.af_step, self.af_max)

        df['psar'] = psar
        df['signal'] = 0
        df.loc[df['Close'] > df['psar'], 'signal'] = 1
        df.loc[df['Close'] < df['psar'], 'signal'] = -1
        return df