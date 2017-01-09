#!/usr/bin/python

import numpy as np
from math import sqrt, exp

class OptionPricer:

    def __init__(self, option, drift, volatility, iter_num=1000, seed=None):
        self.option = option
        self.drift = drift
        self.volatility = volatility
        self.iter_num = iter_num
        self.seed = seed

    def getPrice(self, current_spot, time_adjustment = 0):
        if int(self.option.expiry - time_adjustment) is 0:
            return self.option.payoff(current_spot)

        var = (self.option.expiry - time_adjustment)*self.volatility**2
        root_var = sqrt(var)
        ito_corr = -1*var/2

        moved_spot = current_spot*exp(self.drift*(self.option.expiry-time_adjustment) + ito_corr)
        running_sum = 0

        if self.seed is not None:
            np.random.seed(self.seed)

        if root_var <= 0:
            print("Invalid variance: {}".format(root_var))
        gaussians = np.random.normal(0, root_var, self.iter_num)

        for i in range(self.iter_num):
            running_sum += self.option.payoff(moved_spot*exp(gaussians[i]))

        return running_sum/self.iter_num
