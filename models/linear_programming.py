from scipy.optimize import linprog
import numpy as np

def linear_minimize(data,
                    num_rating=None,
                    rating_at_least=50,
                    method="highs"):
    obj = (data['yield'] / data['dur_mod']).fillna(0).array

    weights_conditions_eq = [
        np.ones(len(obj))
    ]

    weight_conditions_res_eq = [
        1
    ]

    lhs_ineq,rhs_ineq = None, None

    if not num_rating is None:
        lhs_ineq=[num_rating]
        rhs_ineq=[-1 * rating_at_least]

    opt = linprog(c=obj,
                  A_ub=lhs_ineq,
                  b_ub=rhs_ineq,
                  A_eq=weights_conditions_eq,
                  b_eq=weight_conditions_res_eq,
                  method=method)

    return opt['x']
