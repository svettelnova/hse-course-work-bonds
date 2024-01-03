from hacksad.misc import today

import pandas as pd

from backtestad.db.sql.interest_rates import get_rate
from pandas.tseries.offsets import BDay


def get_last_trading_day(date):
    return date + BDay(1) - BDay(1)


def get_swaption_volatility_data(start_date: pd.Timestamp|None = None, end_date: pd.Timestamp|None = None):
    end_date = end_date or today()
    # date: pd.Timestamp = pd.Timestamp(get_last_trading_day(date).date())

    group_codes =   [
        # "DEPO_ICAAP",  # additional to calculate volatility, we have only two points!!!!
        "MOSPRIME",
        "LIBOR",
        "IRS",
        # "IRS_ICAAP",  # bullshit
        "EURIBOR",
        "OIS_ICAAP",
    ]
    rates = get_rate(start_date, end_date,
        group_codes,
        ["RUB"],
    )
    return  rates


    rates_today = rates.set_index("date").sort_index().loc[date]
    group = rates_today.groupby(["date", "base_ccy", "tenor"])
    volatility = group.rate.std()
    return volatility
