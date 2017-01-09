#!/usr/bin/python

import numpy as np
import pandas as pd
from math import exp

class BrownianMotion:

    def __init__(self, drift = 0, variance = 1, seed = None):
        self.drift = drift
        self.variance = variance
        self.seed = seed

    def getValueAt(self, start, time):
        if self.seed is not None:
            np.random.seed(self.seed)

        return start + np.random.normal(self.drift*time, self.variance)

    def getPath(self, start, time, resolution):
        if self.seed is not None:
            np.random.seed(self.seed)

        times = [0]
        path = [start]
        idx = 0

        while times[idx] < time:
            path.append(self.getValueAt(path[idx], resolution))
            times.append(times[idx] + resolution)
            idx += 1

        if times[idx] < time:
            path.append(self.getValueAt(path[idx], time-times[idx]))
            times.append(times[idx] + resolution)

        return pd.Series(path, index=times)

class GeometricBrownianMotion:

    def __init__(self, drift = 0, variance = 1, seed = None):
        self.drift = drift
        self.variance = variance
        self.seed = seed

    def getValueAt(self, start, time):
        if self.seed is not None:
            np.random.seed(self.seed)

        return start*exp(np.random.normal(self.drift*time, self.variance))

    def getPath(self, start, time, resolution):
        if self.seed is not None:
            np.random.seed(self.seed)

        times = [0]
        path = [start]
        idx = 0

        while times[idx] < time:
            path.append(self.getValueAt(path[idx], resolution))
            times.append(times[idx] + resolution)
            idx += 1

        if times[idx] < time:
            path.append(self.getValueAt(path[idx], time-times[idx]))
            times.append(times[idx] + resolution)

        return pd.Series(path, index=times)