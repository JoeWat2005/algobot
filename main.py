from market.data_loader import Market
from strategies.strategy_loader import load_strategies_from_folder
import concurrent.futures
import pandas as pd

# Load OHLCV data
market = Market()
data = market.get_all_data()  # {'AAPL': df, 'MSFT': df, ...}

# Load all strategy classes
strategies = load_strategies_from_folder("strategies")

# Prepare output dict: {ticker: {strategy_name: df_with_signals}}
processed_data = {}

# Worker function to run all strategies on one ticker's data
def process_ticker(ticker, df):
    result = {}
    for strategy in strategies:
        strat_name = strategy.__class__.__name__
        try:
            df_signals = strategy.generate_signals(df.copy())
            if not isinstance(df_signals, pd.DataFrame):
                raise ValueError(f"{strat_name} did not return a DataFrame.")
            result[strat_name] = df_signals
        except Exception as e:
            print(f"Error processing {ticker} with {strat_name}: {e}")
    return ticker, result

# Run strategy processing in parallel across tickers
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(process_ticker, ticker, df) for ticker, df in data.items()]
    for future in concurrent.futures.as_completed(futures):
        ticker, ticker_results = future.result()
        processed_data[ticker] = ticker_results

# Example output for inspection
for ticker, strategies_data in processed_data.items():
    print(f"\n=== Results for {ticker} ===")
    for strat_name, df in strategies_data.items():
        print(f"--- {strat_name} Sample Output ---")
        print(df[['Close', 'signal']].tail(5))

