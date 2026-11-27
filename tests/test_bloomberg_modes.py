from src.providers.bloomberg_provider import fetch_bloomberg_prices


# without a mode, the provider should read the approved sample
default_rows = fetch_bloomberg_prices("AAPL")
sample_rows = fetch_bloomberg_prices("AAPL", mode="APPROVED_SAMPLE")
assert len(default_rows) > 0
assert default_rows == sample_rows
print("Test 1: APPROVED_SAMPLE is the default mode")

# live mode must not pretend to work without an authorized terminal
try:
    fetch_bloomberg_prices("AAPL", mode="LIVE")
except NotImplementedError as error:
    print("Test 2: LIVE mode is not activated:", error)
else:
    raise AssertionError("LIVE mode should raise NotImplementedError")

# a wrong mode name must be refused
try:
    fetch_bloomberg_prices("AAPL", mode="SAMPLE")
except ValueError as error:
    print("Test 3: unknown mode rejected:", error)
else:
    raise AssertionError("unknown mode should raise ValueError")

# a ticker missing from BLOOMBERG_IDENTIFIERS must be refused
try:
    fetch_bloomberg_prices("MSFT")
except KeyError as error:
    print("Test 4: unknown ticker rejected:", error)
else:
    raise AssertionError("unknown ticker should raise KeyError")

print("All Bloomberg mode tests passed!")