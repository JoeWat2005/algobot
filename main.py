from market.data_loader import Market

market = Market()
data = market.get_all_data()

for ticker, df in data.items():
    print(f"{ticker}: {df.shape}")

