# longtrends

A package to download long-term Google Trends.

## Introduction

[Google Trends](https://trends.google.com/trends), downloadable by API using [pytrends](https://pypi.org/project/pytrends/), limits the time period which can be downloaded using a single request. Each request is scaled between 0 and 100, making comparison between different time periods difficult. This package automatically downloads overlapping trends and rescales them, providing trend data across a long-term period.

## Installation

`pip install longtrends`

## Requirements

Requires [pytrends](https://pypi.org/project/pytrends/), installed automatically with `pip`.

## Quick Start

```
from longtrends import LongTrend
from datetime import datetime

keyword = 'suncream'

# Create LongTrend object
longtrend = LongTrend(
                      keyword=keyword,
                      start_date=datetime(2018, 1, 1),
                      end_date=datetime(2022, 3, 31))        # use verbose=True for print output
# Build long-term trends
lt_built = longtrend.build()

# Plot
lt_built.plot(title=f"Google Trends: {longtrend.keyword}", figsize=(15, 3))
```
![suncream.png](/assets/images/suncream.png)
## Under the hood
First, longtrends downloads overlapping trends.
```
from longtrends import rescale_overlaps, get_overlapping_trends, rescaled_longtrend
import pandas as pd

overlapping = get_overlapping_trends(
                                keyword=keyword,
                                start_date=datetime(2018, 1, 1),
                                end_date=datetime(2022, 3, 31),
                                verbose=True)

pd.concat(overlapping, axis=1).plot(figsize=(15,3), legend=False)
```
![overlapping_trends.png](/assets/images/overlapping_trends.png)
Next, i+1th overlap is rescaled to ith overlap.
```
rescaled = rescale_overlaps(overlapping)
pd.concat(rescaled, axis=1).plot(figsize=(15,3), legend=False)
```
![overlaps_rescaled.png](/assets/images/overlaps_rescaled.png)
Finally, a single long-term trend is picked.
```
rescaled = rescaled_longtrend(rescaled)
rescaled.plot(figsize=(15,3), title='Rescaled long-term trend')
```
![rescaled_longtrend.png](/assets/images/rescaled_longtrend.png)

## Disclaimer

This is not an official or supported product. It is provided without warranty under MIT license.
