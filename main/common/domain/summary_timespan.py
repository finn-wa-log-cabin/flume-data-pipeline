from enum import Enum


class SummaryTimespan(Enum):
    """A timespan for a data summmary.

    Values correspond to keys for DateOffset objects in pandas:
    https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects
    """

    DAILY = "D"
    WEEKLY = "W-MON"
    MONTHLY = "MS"
    SEASONAL = "QS-DEC"
    YEARLY = "AS"
