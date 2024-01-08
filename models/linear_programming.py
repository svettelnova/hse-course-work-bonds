from scipy.optimize import linprog
import numpy as np

def linear_minimize(data, method="highs"):
    obj = data['yield_dur'] = data['yield'] / data['dur_mod'].array

    price_today = data.mid.array

    weights_conditions_eq = [
        np.ones(len(obj)),
        price_today
    ]

    weight_conditions_res_eq = [
        1,
        1
    ]

    opt = linprog(c=obj,
                  A_eq=weights_conditions_eq,
                  b_eq=weight_conditions_res_eq,
                  method=method)

    return opt['x']
