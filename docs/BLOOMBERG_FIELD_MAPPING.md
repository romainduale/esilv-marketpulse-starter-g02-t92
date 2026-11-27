# Bloomberg Field Mapping

## 1. Objective and supported modes

The Bloomberg provider converts source-specific market data
into the MarketPulse canonical format. This allows Bloomberg
and Yahoo Finance to share the same analytics functions.

Two modes are supported:

- APPROVED_SAMPLE: reads the instructor-approved local JSON
  file. No Bloomberg Terminal is required.
- LIVE: requires access to an authorized Bloomberg environment.
  The live connection is not implemented at this stage.

The approved sample contains illustrative teaching data,
not certified Bloomberg historical observations.

## 2. Instrument identifiers

| MarketPulse ticker | Bloomberg identifier | Instrument |
|---|---|---|
| AAPL | AAPL US Equity | Apple Inc. |
| SP500 | SPX Index | S&P 500 |

The Bloomberg identifier is used to select the source series.
The canonical ticker is used in the normalized observations.

## 3. Field mapping and data types

| Source field | Canonical field | Python type |
|---|---|---|
| observation_date | date | str (YYYY-MM-DD) |
| canonical_ticker | ticker | str |
| open_value | open | float |
| high_value | high | float |
| low_value | low | float |
| close_value | close | float |
| volume_value | volume | int |

The source JSON contains a list named `series`. Each series
contains a `provider_identifier`, a `canonical_ticker`
and a list of `observations`.

The ticker is obtained from the parent series, while the
six remaining fields come from each individual observation.

The source field names are teaching wrapper keys,
not official Bloomberg field mnemonics.

## 4. Normalization example

The following example uses fictional data for demonstration
purposes only.

### Raw series

```json
{
    "provider_identifier": "AAPL US Equity",
    "canonical_ticker": "AAPL",
    "observations": [
        {
            "observation_date": "2026-11-18",
            "open_value": "100.0",
            "high_value": "112.0",
            "low_value": "99.0",
            "close_value": "110.0",
            "volume_value": "1500"
        }
    ]
}
```

### Canonical observation

```json
{
    "date": "2026-11-18",
    "ticker": "AAPL",
    "open": 100.0,
    "high": 112.0,
    "low": 99.0,
    "close": 110.0,
    "volume": 1500
}
```

Prices are converted to floats and volume to an integer
so that numerical operations can be performed directly.

## 5. Validation and limitations

Before normalization, the provider should check that:

- The canonical ticker is present.
- The observations list is not empty.
- All six required source fields are present.
- No duplicate observation dates exist.

Invalid series should raise an explicit ValueError.

After normalization, each observation must contain exactly
the seven canonical fields with the expected data types.

The normalized observations can be compared with
`data/sample/bloomberg_reference_expected.json`.

Successful execution in APPROVED_SAMPLE mode does not
demonstrate successful LIVE Bloomberg connectivity.