import json
from copy import deepcopy
from pathlib import Path

from src.providers.bloomberg_provider import (
    fetch_bloomberg_prices,
    find_reference_series,
    load_bloomberg_reference_sample,
    normalize_reference_series,
)


def check_prices(prices, ticker):
    assert len(prices) > 0

    expected_keys = {
        "date", "ticker", "open", "high", "low", "close", "volume"
    }

    for row in prices:
        assert set(row) == expected_keys
        assert isinstance(row["date"], str)
        assert row["ticker"] == ticker
        assert isinstance(row["open"], float)
        assert isinstance(row["high"], float)
        assert isinstance(row["low"], float)
        assert isinstance(row["close"], float)
        assert isinstance(row["volume"], int)


aapl = fetch_bloomberg_prices("AAPL", mode="APPROVED_SAMPLE")
sp500 = fetch_bloomberg_prices("SP500", mode="APPROVED_SAMPLE")

check_prices(aapl, "AAPL")
check_prices(sp500, "SP500")
print("Test 1: AAPL and SP500 canonical rows and types OK")

expected_data = json.loads(
    Path("data/sample/bloomberg_reference_expected.json").read_text(
        encoding="utf-8"
    )
)
assert aapl + sp500 == expected_data["rows"]
print("Test 2: Output matches the expected JSON")

payload = load_bloomberg_reference_sample()
valid_series = find_reference_series(payload, "AAPL US Equity")
assert normalize_reference_series(deepcopy(valid_series))
print("Test 3: Complete series accepted")

empty_series = deepcopy(valid_series)
empty_series["observations"] = []

missing_field_series = deepcopy(valid_series)
del missing_field_series["observations"][0]["close_value"]

duplicate_date_series = deepcopy(valid_series)
duplicate_date_series["observations"].append(
    deepcopy(duplicate_date_series["observations"][0])
)

for label, series in [
    ("empty observations", empty_series),
    ("missing close_value", missing_field_series),
    ("duplicate date", duplicate_date_series),
]:
    try:
        normalize_reference_series(series)
    except ValueError as error:
        print(f"Test OK: {label} rejected — {error}")
    else:
        raise AssertionError(f"{label} should raise ValueError")

print("All Bloomberg provider tests passed!")
