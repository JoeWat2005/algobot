from strategies.base import Strategy
import pandas as pd

class RSIStrategy(Strategy):
    def __init__(self, period=14, buy_threshold=30, sell_threshold=70):
        self.period = period
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        # Flatten MultiIndex columns if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        print("\n[RSIStrategy] Input index:", type(df.index))
        print("[RSIStrategy] Input head:")
        print(df.head(3))

        # RSI calculation
        delta = df['Close'].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(self.period).mean()
        avg_loss = loss.rolling(self.period).mean()
        rs = avg_gain / avg_loss
        df['rsi'] = 100 - (100 / (1 + rs))

        # Generate signals
        df['signal'] = 0
        df.loc[df['rsi'] < self.buy_threshold, 'signal'] = 1
        df.loc[df['rsi'] > self.sell_threshold, 'signal'] = -1

        # Debugging output
        print("[RSIStrategy] signal counts:\n", df['signal'].value_counts())

        return df

