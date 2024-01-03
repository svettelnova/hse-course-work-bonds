import math

from pandas import DataFrame
from QuantLib import Actual360
from QuantLib import Period
from QuantLib import QuoteHandle
from QuantLib import SimpleQuote
from QuantLib import SwaptionHelper
from QuantLib import Years


def create_swaption_helpers(data, index, term_structure, engine):
    swaptions = []
    fixed_leg_tenor = Period(20, Years)
    fixed_leg_daycounter = Actual360()
    floating_leg_daycounter = Actual360()
    for d in data:
        vol_handle = QuoteHandle(SimpleQuote(d.volatility))
        helper = SwaptionHelper(
            d.start,  # matrity
            d.length,  # lenth
            vol_handle,  # voltility
            index,  # indx
            fixed_leg_tenor,  # fixdLegTenor
            fixed_leg_daycounter,  # fixdLegDayCounter
            floating_leg_daycounter,  # flotingLegDayCounter
            term_structure,  # terStructure
        )
        helper.setPricingEngine(engine)
        swaptions.append(helper)
    return swaptions


def calibration_report(swaptions, data):
    columns = [
        "Model Price",
        "Market Price",
        "Implied Vol",
        "Market Vol",
        "Rel Er\
    ror Price",
        "Rel Error Vols",
    ]
    report_data = []
    cum_err = 0.0
    cum_err2 = 0.0
    for i, s in enumerate(swaptions):
        model_price = s.modelValue()
        market_vol = data[i].volatility
        black_price = s.blackPrice(market_vol)
        rel_error = model_price / black_price - 1.0
        implied_vol = s.impliedVolatility(model_price, 1e-5, 50, 0.0, 0.50)
        rel_error2 = implied_vol / market_vol - 1.0
        cum_err += rel_error * rel_error
        cum_err2 += rel_error2 * rel_error2
        report_data.append(
            (model_price, black_price, implied_vol, market_vol, rel_error, rel_error2)
        )
    print("Cumulative Error Price: %7.5f" % math.sqrt(cum_err))
    print("Cumulative Error Vols : %7.5f" % math.sqrt(cum_err2))
    return DataFrame(report_data, columns=columns, index=[""] * len(report_data))
