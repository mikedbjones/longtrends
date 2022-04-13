# longtrends

A package to download long-term Google Trends.

## Introduction

[Google Trends](https://trends.google.com/trends), downloadable by API using [pytrends](https://pypi.org/project/pytrends/), limits the time period which can be downloaded using a single request. Each request is scaled between 0 and 100, making comparison between different time periods difficult. This package automatically downloads overlapping trends and rescales them, providing trend data across a long-term period.

## Installation

`pip install longtrends`

## Requirements

Requires [pytrends](https://pypi.org/project/pytrends/), installed automatically with `pip`.

## Usage

```
from longtrends import rescale_overlaps, get_overlapping_trends
from datetime import datetime, timedelta

google = get_overlapping_trends(
                                keyword='google',
                                start_date=datetime(2021, 1, 1),
                                end_date=datetime(2021, 1, 31),
                                days_delta=30)

google_rescaled = rescale_overlaps(google)
google_rescaled.plot()
```

## Disclaimer

This is not an official or supported product. It is provided without warranty under MIT license.
