from market.data_loader import Market

market = Market()
data = market.get_data("AAPL", "2020-01-01", "2024-01-01")
print(data.head)
