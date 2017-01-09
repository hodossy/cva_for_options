#!/usr/bin/python

import os, sys
import numpy as np
import pandas as pd
from optparse import OptionParser
from brownian_motion import GeometricBrownianMotion
from option_pricer import Option, OptionPricer

def reprint_last(msg):
    sys.stdout.write('\r')
    sys.stdout.flush()
    print(msg)

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-a", "--alpha", dest="alpha",
                      default="0.001", type=float,
                      help="Default probability coefficient. Default is 0.001")

    parser.add_option("-e", "--expiry", dest="expiry",
                      default="52", type=float,
                      help="Expiry of the option in weeks. Default is 52.")

    parser.add_option("-i", "--iterations", dest="iter_num",
                      default="1000", type=int,
                      help="Iteration number of the Monte Carlo simulation. Default is 1000.")

    parser.add_option("-p", "--price-history", dest="src",
                      help="Weekly data of stock prices.",
                      metavar="FILE")

    parser.add_option("-r", "--resolution", dest="resolution",
                      default="1", type=float,
                      help="Resolution of time for the simulation. Default is 1.")

    parser.add_option("-s", "--strike", dest="strike",
                      type=float,
                      help="Strike of the option")

    parser.add_option("--seed", dest="seed",
                      type=float,
                      help="Seed for the random number generator.")

    parser.add_option("-t", "--type", dest="opt_type",
                      type="choice", choices=["call", "put"],
                      default="put", help="Type of option to price. Default is PUT.")

    ( options, args ) = parser.parse_args()

    options.src = os.path.abspath(options.src)

    payoff = None

    if options.opt_type == "call":
        payoff = lambda x, y = options.strike: max(x-y,0)
    else:
        payoff = lambda x, y = options.strike: max(y-x,0)

    option = Option(payoff, options.expiry)

    data = pd.read_csv(options.src, sep=',', decimal='.')

    drift = data["Adjusted_Close_PCT"].mean()
    volatility = data["Adjusted_Close_PCT"].std()

    print("Observed drift is {}.".format(drift))
    print("Observed volatility is {}".format(volatility))

    option_pricer = OptionPricer(option, drift, volatility, options.iter_num)

    current_spot = data["Adjusted_Close"][0]
    print("Current spot is {}".format(current_spot))

    print("Simulating stock price evolution...0 %", end="\r")
    gbm = GeometricBrownianMotion(drift, volatility, options.seed)

    loss_ratio = None
    percent = int(options.iter_num / 100)
    for i in range(options.iter_num):
        losses = {}
        for index, value in gbm.getPath(current_spot, options.expiry, options.resolution).iteritems():
            losses[index] = option_pricer.getPrice(value, index) / value
        if loss_ratio is None:
            loss_ratio = pd.DataFrame(losses,index=[i])
        else:
            loss_ratio = loss_ratio.append(pd.DataFrame(losses,index=[i]))
        if i % percent is 0:
            print("Simulating stock price evolution...{} %".format(int(i / percent)), end="\r")
    print("Simulating stock price evolution...100 %")

    running_sum = 0
    for time in loss_ratio.columns:
        running_sum += loss_ratio[time].mean()

    print("Estimated option price is {}".format(option_pricer.getPrice(current_spot)))
    print("Estimated CVA is {}.".format(options.alpha*current_spot*options.resolution*running_sum))