from src.providers.yahoo_provider import fetch_prices_for_ticker


def check_prices(prices, ticker):
    assert len(prices) > 0

    for row in prices:
        assert isinstance(row["date"], str)
        assert row["ticker"] == ticker
        assert isinstance(row["ticker"], str)
        assert isinstance(row["open"], float)
        assert isinstance(row["high"], float)
        assert isinstance(row["low"], float)
        assert isinstance(row["close"], float)
        assert isinstance(row["volume"], int)


aapl = fetch_prices_for_ticker("AAPL")
check_prices(aapl, "AAPL")
print("Test 1: AAPL data and types OK")

sp500 = fetch_prices_for_ticker("SP500")
check_prices(sp500, "SP500")
print("Test 2: SP500 data and types OK")

aapl_3m = fetch_prices_for_ticker(
    "AAPL", period="3mo", interval="1d"
)
check_prices(aapl_3m, "AAPL")
assert len(aapl_3m) > len(aapl)
print("Test 3: Custom period OK")

try:
    fetch_prices_for_ticker("UNKNOWN")
except ValueError as error:
    print("Test 4: Unknown ticker OK:", error)
else:
    raise AssertionError("Expected ValueError")

print("All Yahoo provider tests passed!")