from strategies.base import Strategy
import pandas as pd

class EnvelopeChannelStrategy(Strategy):
    def __init__(self, window=20, percentage=0.025):
        self.window = window
        self.percentage = percentage

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        # Flatten MultiIndex columns if needed
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        print("\n[EnvelopeChannelStrategy] Input index:", type(df.index))
        print("[EnvelopeChannelStrategy] Input head:")
        print(df.head(3))

        # Calculate moving average and envelopes
        ma = df['Close'].rolling(self.window).mean()
        upper_envelope = ma * (1 + self.percentage)
        lower_envelope = ma * (1 - self.percentage)

        # Align everything with 'Close'
        ma, close = ma.align(df['Close'], axis=0)
        upper_envelope, _ = upper_envelope.align(df['Close'], axis=0)
        lower_envelope, _ = lower_envelope.align(df['Close'], axis=0)

        # Assign calculated columns
        df['ma'] = ma
        df['upper_envelope'] = upper_envelope
        df['lower_envelope'] = lower_envelope

        # Generate signals
        df['signal'] = 0
        df.loc[close > upper_envelope, 'signal'] = -1  # Price too high — sell
        df.loc[close < lower_envelope, 'signal'] = 1   # Price too low — buy

        print("[EnvelopeChannelStrategy] signal counts:\n", df['signal'].value_counts())

        return df

