# Checkpoint B

## Student

- Name: Roman Cianci
- GitHub: @RomanCianci

## Contribution

- Branches:
  - feature/display-market-metadata
  - feature/yahoo-provider
  - feature/yahoo-provider-compliance
- Main commits:
  - b5e3bdf
  - 5f4261a
  - 419eda4
  - 8b6ab2a
  - e6d7665
  - cb48f5b
  - b660ad9
  - 730fba5
- Pull Requests: #1, #6, #8
- Reviewed Pull Requests: #3, #4

## Work completed

- Display market observation dates.
- Integrate Yahoo Finance.
- Compare AAPL and SP500 over one month.
- Integrate the shared analytics module.
- Resolve the analytics merge conflict.
- Implement the complete OHLCV data format.
- Implement the Yahoo symbol mapping.
- Implement `fetch_yahoo_prices()` and `fetch_prices_for_ticker()`.
- Validate Yahoo data types, custom periods and unknown tickers.
- Successfully execute all six analytics tests and four Yahoo provider tests.

## Main difficulty

Resolving the merge conflict, integrating the shared analytics module
and ensuring that the Yahoo Finance provider respects the canonical
MarketPulse data format.

## Evidence

- `01_pull_request.png`
- `02_code_review.png`
- `03_yahoo_market_data.png`
- `04_instrument_benchmark.png`
