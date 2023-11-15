"""
Bond portfolio optimization with limit constraints
"""
import typing as tp
from datetime import datetime

import numpy as np
import pandas as pd
import scipy.optimize as sco


class OFZSharpRatio:
    """
    Calculate Sharpe ratio
    """

    def __init__(self, raw_bond_data: pd.DataFrame, value_date, maturity_limit):
        """
        smf
        """
        self.maturity_limit = maturity_limit

        self.bond_data = raw_bond_data
        self.bond_data["yield"] = self.bond_data["yield"].fillna(0)
        assert not self.bond_data.isna().any().any(), (
            f"nans in data: " f"{self.bond_data.isna().any()}"
        )

    @property
    def bonds_mod_dur(self):
        """
        bonds_mod_dur
        """
        return self.bond_data.dur_mod

    def __call__(self, weights) -> np.ndarray:
        """
        calculate custom sharpe ratio
        sharp = (overvaluation - penalty) / portfolio_mod_dur
        """
        overvaluation = np.dot(self.bond_data["yield"], weights)
        portfolio_mod_dur = np.dot(self.bonds_mod_dur, weights)
        value = -overvaluation / portfolio_mod_dur

        return value


def create_constraints(
    target_rating: float, ratings: np.ndarray
) -> tuple[dict[str, tp.Callable], ...]:
    """
    create constraint based on the given params
    """
    default = {"type": "eq", "fun": lambda x: 1 - np.sum(x)}  # todo rm hardcode
    rating = {"type": "ineq", "fun": lambda x: np.average(ratings * x) - target_rating}
    return default, rating


def get_optimal_weights(
    bond_data: pd.DataFrame,
    upper_bound: float,
    value_date: pd.Timestamp,
    maturity_limit: int,
    fee: float = 0,
    target_rating: float = 90,
):
    """
    Find optimal weights by maximizing custom sharp ratio
    """
    _ = fee
    sharp_ratio = OFZSharpRatio(
        bond_data,
        value_date,
        maturity_limit,
    )
    asset_num = len(bond_data)
    init_weights = np.ones(asset_num) / asset_num
    assert upper_bound >= 1 / asset_num, "not enough assets for the given upper_bound"
    constraints = create_constraints(
        target_rating=target_rating, ratings=sharp_ratio.bond_data.num_rating
    )
    bounds = tuple((0, upper_bound) for _ in range(asset_num))
    weights = sco.minimize(
        fun=sharp_ratio,
        x0=init_weights,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
        options={
            "maxiter": 1000,
            "ftol": 1e-6,
        },
    )
    # check total sum limit
    final_sum = sum(weights["x"])
    assert round(final_sum, 2) == 1, (
        f"optimized weights don't sum up to one:" f" sum = {final_sum}"
    )
    if weights["fun"] > 0:
        raise ValueError("Failed to optimize")
    return weights["x"]


if __name__ == "__main__":
    bond_data = pd.DataFrame(
        {
            "mid": {
                (datetime(2023, 9, 20), "RU000A0GN9A7"): 0.72419,
                (datetime(2023, 9, 20), "RU000A0JV4N8"): 1.03248,
                (datetime(2023, 9, 20), "RU000A0JWDN6"): 0.7545999999999999,
                (datetime(2023, 9, 20), "RU000A0JV4Q1"): 1.0378,
                (datetime(2023, 9, 20), "RU000A0JVA10"): 1.0073,
                (datetime(2023, 9, 20), "RU000A0JW0S4"): 0.8599,
                (datetime(2023, 9, 20), "RU000A0JUMH3"): 0.97,
            },
            "yield": {
                (datetime(2023, 9, 20), "RU000A0GN9A7"): 0.11516907630756,
                (datetime(2023, 9, 20), "RU000A0JV4N8"): 0.081891139010426,
                (datetime(2023, 9, 20), "RU000A0JWDN6"): 0.11854594173911,
                (datetime(2023, 9, 20), "RU000A0JV4Q1"): 0.082937393334456,
                (datetime(2023, 9, 20), "RU000A0JVA10"): 0.13269342447362,
                (datetime(2023, 9, 20), "RU000A0JW0S4"): 0.12751130545082,
                (datetime(2023, 9, 20), "RU000A0JUMH3"): 0.11584644614069,
            },
            "dur_mod": {
                (datetime(2023, 9, 20), "RU000A0GN9A7"): 6.657464466758817,
                (datetime(2023, 9, 20), "RU000A0JV4N8"): 5.636553190617984,
                (datetime(2023, 9, 20), "RU000A0JWDN6"): 2.2740818185644334,
                (datetime(2023, 9, 20), "RU000A0JV4Q1"): 6.702875676271667,
                (datetime(2023, 9, 20), "RU000A0JVA10"): 1.1777322386699,
                (datetime(2023, 9, 20), "RU000A0JW0S4"): 1.8557544966646666,
                (datetime(2023, 9, 20), "RU000A0JUMH3"): 0.5881085107021066,
            },
            "num_rating": {
                (datetime(2023, 9, 20), "RU000A0GN9A7"): 00,
                (datetime(2023, 9, 20), "RU000A0JV4N8"): 0,
                (datetime(2023, 9, 20), "RU000A0JWDN6"): 0,
                (datetime(2023, 9, 20), "RU000A0JV4Q1"): 0,
                (datetime(2023, 9, 20), "RU000A0JVA10"): 0,
                (datetime(2023, 9, 20), "RU000A0JW0S4"): 90,
                (datetime(2023, 9, 20), "RU000A0JUMH3"): 95,
            },
        }
    )
    new_weights = get_optimal_weights(
        bond_data=bond_data,
        upper_bound=0.5,
        value_date=pd.Timestamp("2023-09-20 20:00:00"),
        maturity_limit=10,
    )
    print(new_weights)
