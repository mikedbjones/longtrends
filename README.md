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
from datetime import datetime

# Get overlapping trends
olympics = get_overlapping_trends(
                                keyword='olympics',
                                start_date=datetime(2021, 7, 4),
                                end_date=datetime(2021, 8, 29),
                                days_delta=10)

# Rescale overlaps
olympics_rescaled = rescale_overlaps(olympics)

# Optionally, plot the two sets of trends for comparison
import matplotlib.pyplot as plt
import pandas as pd

def trends_plot(trends_list):

    """
    Args:
        trends_list (list): list of Series of trends, with scores as columns and dates as index

            each Series eg:

                date
                2016-04-10      44
                2016-04-17      44
                2016-04-24     100

    Returns:
        NoneType

    """

    # concat the trends together
    df = pd.concat(trends_list, axis=1)

    df.columns = [f'{df.columns[i]}_{i}' for i in range(df.shape[1])]
    df.plot.line(figsize=(15, 4))
    plt.ylabel('Score')
    plt.title('Google Trends over different time periods')
    plt.legend()
    plt.show()

# Plot overlapping trends
trends_plot(olympics)

# Plot rescaled trends
trends_plot(olympics_rescaled)
```

## Images

Plot outputs from the above usage example:

1. Trends for 'olympics', before rescaling between overlaps:

![olympics_overlapping.png](/assets/images/olympics_overlapping.png)

2. Trends after rescaling

![olympics_rescaled.png](/assets/images/olympics_rescaled.png)

## Disclaimer

This is not an official or supported product. It is provided without warranty under MIT license.
