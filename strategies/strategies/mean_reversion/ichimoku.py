from strategies.base import Strategy
import pandas as pd

class IchimokuCloudStrategy(Strategy):
    def __init__(self):
        self.tenkan_window = 9
        self.kijun_window = 26
        self.senkou_span_b_window = 52

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        # Flatten MultiIndex columns if necessary
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        print("\n[IchimokuCloudStrategy] Input index:", type(df.index))
        print("[IchimokuCloudStrategy] Input head:")
        print(df.head(3))

        # Tenkan-sen
        high_9 = df['High'].rolling(window=self.tenkan_window).max()
        low_9 = df['Low'].rolling(window=self.tenkan_window).min()
        tenkan_sen = (high_9 + low_9) / 2

        # Kijun-sen
        high_26 = df['High'].rolling(window=self.kijun_window).max()
        low_26 = df['Low'].rolling(window=self.kijun_window).min()
        kijun_sen = (high_26 + low_26) / 2

        # Senkou Span A = (tenkan + kijun)/2, shifted forward 26 periods
        senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(self.kijun_window)

        # Senkou Span B = (highest high + lowest low) / 2 over 52 periods, shifted
        high_52 = df['High'].rolling(window=self.senkou_span_b_window).max()
        low_52 = df['Low'].rolling(window=self.senkou_span_b_window).min()
        senkou_span_b = ((high_52 + low_52) / 2).shift(self.kijun_window)

        # Align everything with 'Close'
        tenkan_sen, close = tenkan_sen.align(df['Close'], axis=0)
        kijun_sen, _ = kijun_sen.align(df['Close'], axis=0)
        senkou_span_a, _ = senkou_span_a.align(df['Close'], axis=0)
        senkou_span_b, _ = senkou_span_b.align(df['Close'], axis=0)

        # Assign to DataFrame for diagnostics / plotting
        df['tenkan_sen'] = tenkan_sen
        df['kijun_sen'] = kijun_sen
        df['senkou_span_a'] = senkou_span_a
        df['senkou_span_b'] = senkou_span_b

        # Generate signals
        df['signal'] = 0
        df.loc[close > senkou_span_a, 'signal'] = 1
        df.loc[close < senkou_span_b, 'signal'] = -1

        print("[IchimokuCloudStrategy] signal counts:\n", df['signal'].value_counts())

        return df
