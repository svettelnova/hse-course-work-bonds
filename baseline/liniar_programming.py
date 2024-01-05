from collections.abc import Callable
from typing import Literal

import numpy as np
from scipy.optimize import Bounds
from scipy.optimize import LinearConstraint
from scipy.optimize import linprog
from scipy.optimize import NonlinearConstraint
from scipy.optimize import OptimizeResult


Constraint = LinearConstraint | NonlinearConstraint


def minimize(
    data,
    x0: np.ndarray[float],
    method: Literal["highs", "highs-ds", "highs-ipm"] = "highs",
    jac: Callable | Literal["2-point", "3-point", "cs"] | bool = None,
    hess: Callable | Literal["2-point", "3-point", "cs"] = None,
    bounds: tuple[Bounds] = (),
    constraints: tuple[Constraint] = (),
    maxiter: int = 1_000,
    ftol: float = 1e-6,
) -> OptimizeResult:
    """
    Minimize approximated sharpe raio using LP

    sum[yield] / sum[duration] ~ sum[yield_i / duration_i]

    use `results['x']` to access optimal weights
    """
    method = method or "highs"
    valid_methods = ("highs", "highs-ds", "highs-ipm")
    if method not in valid_methods:
        raise ValueError(f"unknown {method = }, expected one of {valid_methods}")
    _, _, _, _ = method, jac, hess, constraints

    #
    # new scipy bounds to old bounds
    #

    old_bounds = []
    if bounds:
        lb, ub = bounds.lb, bounds.ub
        old_bounds = np.vstack((lb, ub)).T.tolist()

    sharpe = data.z_spread / data.mod_dur
    sharpe[sharpe < 0] = 0  # only positive sharpe ratio cuz ve can't short

    #  z * x > z.median, sigma * x < sigma.median
    A_ub = np.vstack([-data.z_spread, data.mod_dur])
    mod_dur_bound = np.min((data.mod_dur.mean(), data.mod_dur.median()))

    b_ub = np.array([-data.z_spread.median(), mod_dur_bound])

    A_eq = np.ones((1, data.z_spread.size))  # sum of weight is 1

    result = linprog(
        c=-1 * sharpe,
        A_ub=A_ub,
        b_ub=b_ub,
        A_eq=A_eq,
        b_eq=1,
        bounds=old_bounds,
        method="highs",
        options={
            "maxiter": maxiter,
            "tol": ftol,
        },
    )
    return result
