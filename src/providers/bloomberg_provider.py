"""Bloomberg data provider for MarketPulse approved sample data."""

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]

CANDIDATE_PATHS = [
    REPO_ROOT / "data/sample/bloomberg_reference_sample.json",
    Path("data/sample/bloomberg_reference_sample.json"),
    Path("../data/sample/bloomberg_reference_sample.json"),
    Path("../../data/sample/bloomberg_reference_sample.json"),
]

BLOOMBERG_IDENTIFIERS = {
    "AAPL": "AAPL US Equity",
    "SP500": "SPX Index",
}

REQUIRED_FIELDS = {
    "observation_date",
    "open_value",
    "high_value",
    "low_value",
    "close_value",
    "volume_value",
}


def get_reference_sample_path():
    """Return the first existing path to the approved Bloomberg sample."""
    for path in CANDIDATE_PATHS:
        if path.exists():
            return path

    searched_paths = ", ".join(str(path) for path in CANDIDATE_PATHS)
    raise FileNotFoundError(
        f"Bloomberg reference sample not found. Searched: {searched_paths}"
    )


def load_bloomberg_reference_sample(path=None):
    """Load the approved reference JSON payload."""
    target_path = Path(path) if path is not None else get_reference_sample_path()

    with target_path.open(encoding="utf-8") as file:
        return json.load(file)


def find_reference_series(payload, provider_identifier):
    """Find a Bloomberg series by its provider-specific identifier."""
    if not isinstance(payload, dict) or not isinstance(payload.get("series"), list):
        raise ValueError("Invalid Bloomberg sample: expected a 'series' list.")

    for series in payload["series"]:
        if (
            isinstance(series, dict)
            and series.get("provider_identifier") == provider_identifier
        ):
            return series

    raise ValueError(
        "Approved Bloomberg series not found for identifier: "
        f"{provider_identifier}"
    )


def validate_reference_series(series):
    """Raise ValueError if a reference series cannot be normalized safely."""
    if not isinstance(series, dict):
        raise ValueError("Invalid Bloomberg series: expected a dictionary.")

    ticker = series.get("canonical_ticker")
    if not isinstance(ticker, str) or not ticker.strip():
        raise ValueError("Invalid Bloomberg series: missing canonical_ticker.")

    observations = series.get("observations")
    if not isinstance(observations, list) or not observations:
        raise ValueError("Invalid Bloomberg series: observations must be a non-empty list.")

    seen_dates = set()

    for index, observation in enumerate(observations):
        if not isinstance(observation, dict):
            raise ValueError(f"Observation {index} must be a dictionary.")

        missing = REQUIRED_FIELDS - set(observation)
        if missing:
            raise ValueError(
                f"Observation {index} is missing fields: {', '.join(sorted(missing))}"
            )

        date = observation["observation_date"]
        if not isinstance(date, str) or not date:
            raise ValueError(f"Observation {index} has an invalid observation_date.")

        if date in seen_dates:
            raise ValueError(f"Duplicate observation date: {date}")
        seen_dates.add(date)

        try:
            for field in ("open_value", "high_value", "low_value", "close_value"):
                float(observation[field])
            int(observation["volume_value"])
        except (TypeError, ValueError) as error:
            raise ValueError(
                f"Observation {index} contains a non-numeric price or volume."
            ) from error


def normalize_reference_series(series):
    """Convert a Bloomberg series into canonical MarketPulse rows."""
    validate_reference_series(series)

    ticker = series["canonical_ticker"]
    rows = []

    for observation in series["observations"]:
        rows.append(
            {
                "date": observation["observation_date"],
                "ticker": ticker,
                "open": float(observation["open_value"]),
                "high": float(observation["high_value"]),
                "low": float(observation["low_value"]),
                "close": float(observation["close_value"]),
                "volume": int(observation["volume_value"]),
            }
        )

    return rows


def fetch_approved_sample_prices(provider_identifier, sample_path=None):
    """Load, select, and normalize one series from the approved sample."""
    payload = load_bloomberg_reference_sample(sample_path)
    series = find_reference_series(payload, provider_identifier)
    return normalize_reference_series(series)


def fetch_raw_bloomberg_history(identifier, start_date=None, end_date=None):
    """Placeholder for a future authorized Bloomberg Terminal connection."""
    raise NotImplementedError(
        "Live Bloomberg access requires an authorized trading-room terminal."
    )


def fetch_bloomberg_prices(ticker, mode="APPROVED_SAMPLE"):
    """Return Bloomberg prices for a canonical ticker."""
    if ticker not in BLOOMBERG_IDENTIFIERS:
        raise KeyError(f"Unknown canonical ticker for Bloomberg provider: {ticker}")

    provider_identifier = BLOOMBERG_IDENTIFIERS[ticker]

    if mode == "APPROVED_SAMPLE":
        return fetch_approved_sample_prices(provider_identifier)

    if mode == "LIVE":
        return fetch_raw_bloomberg_history(provider_identifier)

    raise ValueError(f"Unrecognized Bloomberg mode: {mode}")
