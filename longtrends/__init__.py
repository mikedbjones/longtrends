from pytrends.request import TrendReq
import pandas as pd
from datetime import timedelta

def get_trends(keyword, start_date, end_date, verbose=False):

    """
    Args:
        keyword (str): The search term to download trends for
        start_date (datetime.datetime): The start date for the search
        end_date (datetime.datetime): The end date for the search

    Returns:
        trends (pd.Series): trends for search term across date range, with index as date

            eg:

                date
                2016-04-10     44
                2016-04-17     42
                2016-04-24     100
                ...            ...

    """

    # timeout prevents code from hanging if server does not respond
    # retries allows request to be tried again in case of failure
    # backoff_factor will delay attempts between retries
    # more details at https://github.com/GeneralMills/pytrends
    pytrend = TrendReq(timeout=(10,25), retries=2, backoff_factor=0.1)
    timeframe = f'{start_date.strftime("%Y-%m-%d")} {end_date.strftime("%Y-%m-%d")}'
    pytrend.build_payload([keyword], timeframe=timeframe)

    if verbose == True:
        print(f'Downloading {(end_date - start_date).days + 1} days of trends for {keyword} between {start_date} and {end_date}')

    trends_df = pytrend.interest_over_time()

    # keep only full periods of data, then drop isPartial column
    # force string type to avoid numpy interpreting isPartial as boolean
    # empty results will not include isPartial column
    if not trends_df.empty:
        trends_df['isPartial'] = trends_df['isPartial'].astype(str)
        trends_df = trends_df[trends_df['isPartial'] == 'False']
        trends_df = trends_df.drop(columns=['isPartial'])

    trends = trends_df.squeeze()

    return trends

def get_overlapping_trends(keyword, start_date, end_date, days_delta=270, verbose=False):

    """
    Args:
        keyword (str): The search term to download trends for
        start_date (datetime.datetime): The start date for the search
        end_date (datetime.datetime): The end date for the search
        days_delta (int): length of each trends result to download

    Returns:
        trends_list (list): list of Series with overlapping trends
            The first Series has half the number of rows of the subsequent Series
            Each adjacent pair overlaps by days_delta/2

            Eg, the first three elements of trends_list may look like:

                trends_list[0]:

                date
                2021-07-04     100
                2021-07-05      86
                2021-07-06      75
                2021-07-07      79
                2021-07-08      90

                trends_list[1]:

                date
                2021-07-04      77
                2021-07-05      67
                2021-07-06      58
                2021-07-07      61
                2021-07-08      69
                2021-07-09      62
                2021-07-10      60
                2021-07-11      99
                2021-07-12      86
                2021-07-13     100
                2021-07-14      79

                trends_list[2]:

                date
                2021-07-09      33
                2021-07-10      32
                2021-07-11      53
                2021-07-12      46
                2021-07-13      54
                2021-07-14      42
                2021-07-15      42
                2021-07-16      48
                2021-07-17      65
                2021-07-18      84
                2021-07-19     100

    Raises:
        ValueError: if days_delta is not even
        ValueError: if days_delta > 270
        ValueError: if start_date and end_date are not at least days_delta days apart

    Notes:
        - First, the function looks for the first days_delta/2 weeks of trend history
        - Then it finds all sets of days_delta weeks after this, each overlapping by days_delta/2
        - If no trends are found, returns a pair of empty Series

    """

    if days_delta > 270:
        raise ValueError('days_delta must be <= 270')

    if days_delta % 2 != 0:
        raise ValueError('days_delta must be even')

    if (end_date - start_date).days + 1 <= days_delta:
        raise ValueError('start_date and end_date must be at least days_delta days apart. Use get_trends() to get short-term trends')

    trends_list = []
    start_dates = []

    # keep track of whether first days_delta/2 weeks have been successfully downloaded
    first_half = False

    while not first_half:
        # get first half-period result
        first_plus_half = start_date + timedelta(days=0.5*days_delta-1)
        if verbose == True:
            print(f'Trying first {int(0.5*days_delta)} days of trends for \'{keyword}\'')
        trends = get_trends(keyword, start_date, first_plus_half, verbose)

        # if no trends were found, series will be empty.
        if trends.empty:
            if verbose == True:
                print('None found')
            # shift start_date on half a period for next try
            start_date += timedelta(days=0.5*days_delta)

            # if no first half-period can be found, return a pair of empty series
            if start_date > end_date:
                return [trends, trends]
        else:
            if verbose == True:
                print('Downloaded successfully')
            trends_list.append(trends)
            first_half = True

    next_date = start_date
    while next_date < end_date:
        start_date = next_date

        # check this period has not already been downloaded. If it has, break
        if start_date not in start_dates:
            start_dates.append(start_date)

            start_date_plus = start_date + timedelta(days=min(days_delta-1, (end_date - start_date).days))
            trends = get_trends(keyword, start_date, start_date_plus, verbose)

            # if no trends found, return a pair of empty series
            if trends.empty:
                print('None found')
                return [pd.Series(), pd.Series()]
            else:
                trends_list.append(trends)

            if start_date_plus == end_date:
                next_date = end_date
            else:
                next_date = start_date + timedelta(days=0.5*days_delta)

        else:
            break

    return trends_list

def ext_scale(to_scale, scale_by):
    """

    Args:
        to_scale (pd.Series): the Series to scale

            eg:

                date
                2021-07-04    100
                2021-07-05     86
                2021-07-06     75
                2021-07-07     79
                2021-07-08     90

        scale_by (pd.Series): the Series to scale by

            eg:

                date
                2021-07-04     77
                2021-07-05     67
                2021-07-06     58
                2021-07-07     61
                2021-07-08     69
                2021-07-09     62
                2021-07-10     60
                2021-07-11     99
                2021-07-12     86
                2021-07-13    100

    Returns:
        scaled (pd.Series): to_scale scaled by scale_by

            eg:

                date
                2021-07-04    100.000000
                2021-07-05     86.842105
                2021-07-06     75.000000
                2021-07-07     78.947368
                2021-07-08     89.473684
                2021-07-09     80.263158
                2021-07-10     77.631579
                2021-07-11    128.947368
                2021-07-12    111.842105
                2021-07-13    130.263158

    Raises:
        ValueError: if overlapping part of to_scale with scale_by has range 0, which would lead to divide by zero

    """

    # find intersections
    overlap = [i for i in to_scale.index if i in scale_by.index]
    inter_ts = to_scale.loc[overlap]
    inter_sb = scale_by.loc[overlap]

    factor = inter_sb.max() - inter_sb.min()

    if inter_ts.max() - inter_ts.min() == 0:
        raise ValueError('unable to scale: to_scale has range 0 in overlap with scale_by; this may be because of an extreme spike in trend data')

    scaled = factor * (to_scale - inter_ts.min()) / (inter_ts.max() - inter_ts.min())
    scaled += inter_sb.min()
    return scaled

def rescale_overlaps(trends_list):
    """

    Args:
        trends_list (list): list of overlapping Series of trends, with scores as columns and dates as index

    Returns:
        trends_list_scaled(list): trends_list scaled using overlaps between ith and (i+1)th elements
    """

    trends_list_scaled = []
    trends_list_scaled.append(trends_list[0])

    for i in range(len(trends_list)-1):
        es = ext_scale(trends_list[i+1], trends_list_scaled[i])
        trends_list_scaled.append(es)

    return trends_list_scaled

def rescaled_longtrend(trends_list_scaled):
    longtrend = pd.DataFrame(pd.concat(trends_list_scaled)).reset_index().drop_duplicates(subset='date').set_index('date').squeeze()
    rescaled = 100 * (longtrend - longtrend.min()) / (longtrend.max() - longtrend.min())
    return rescaled

class LongTrend():
    def __init__(self, keyword, start_date, end_date):
        self.keyword = keyword
        self.start_date = start_date
        self.end_date = end_date

    def build(self, **kwargs):
        ot = get_overlapping_trends(self.keyword, self.start_date, self.end_date, **kwargs)
        ro = rescale_overlaps(ot)
        rl = rescaled_longtrend(ro)
        return rl
