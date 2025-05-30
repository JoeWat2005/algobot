import sys
import os
from datetime import datetime
from market.data_loader import Market
from strategies.strategy_loader import load_strategies_from_folder
import concurrent.futures
import pandas as pd

# Logger setup
class Logger:
    def __init__(self, log_path="logs/debug_log.txt"):
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        self.terminal = sys.stdout
        self.log = open(log_path, "w", encoding="utf-8")
        self.err_log = open(log_path.replace(".txt", "_errors.txt"), "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        if "Error" in message or "Exception" in message or "Traceback" in message:
            self.err_log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()
        self.err_log.flush()

    def close(self):
        self.log.close()
        self.err_log.close()

if __name__ == "__main__":
    logger = Logger("logs/debug_log.txt")
    sys.stdout = sys.stderr = logger

    try:
        print(f"\n[{datetime.now()}] Starting strategy processing...")

        # Load OHLCV data
        market = Market()
        data = market.get_all_data()  # {'AAPL': df, 'MSFT': df, ...}

        # Load all strategy classes
        strategies = load_strategies_from_folder("strategies")

        # Prepare output dict
        processed_data = {}

        # Worker function
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

        # Run strategy processing in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_ticker, ticker, df) for ticker, df in data.items()]
            for future in concurrent.futures.as_completed(futures):
                ticker, ticker_results = future.result()
                processed_data[ticker] = ticker_results

        # Output results
        for ticker, strategies_data in processed_data.items():
            print(f"\n=== Results for {ticker} ===")
            for strat_name, df in strategies_data.items():
                print(f"--- {strat_name} Sample Output ---")
                print(df[['Close', 'signal']].tail(5))

        print(f"\n[{datetime.now()}] Strategy processing completed.")

    finally:
        logger.close()
