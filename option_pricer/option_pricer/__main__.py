#!/usr/bin/python

from optparse import OptionParser
from .option import Option
from .option_pricer import OptionPricer

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-e", "--expiry", dest="expiry",
                      default="52", type=float,
                      help="Expiry of the option in weeks. Default is 52.")

    parser.add_option("-d", "--drift", dest="drift",
                      default="0", type=float,
                      help="Drift of the underlying stock in %. Default is 0.")

    parser.add_option("-i", "--iterations", dest="iter_num",
                      default="1000", type=int,
                      help="Iteration number of the Monte Carlo simulation. Default is 1000.")

    parser.add_option("-p", "--spot", dest="spot",
                      type=float, default="0",
                      help="Current spot of the underlying stock. Default is 0.")

    parser.add_option("-s", "--strike", dest="strike",
                      type=float,
                      help="Strike of the option")

    parser.add_option("--seed", dest="seed",
                      type=float,
                      help="Seed for the random number generator.")

    parser.add_option("-t", "--type", dest="opt_type",
                      type="choice", choices=["call", "put"],
                      default="put", help="Type of option to price. Default is PUT.")

    parser.add_option("-v", "--volatility", dest="volatility",
                      default="1", type=float,
                      help="Volatility of the underlying stock in %. Default is 1.")

    ( options, args ) = parser.parse_args()

    options.drift /= 100
    options.volatility /= 100

    payoff = None

    if options.opt_type is "call":
        payoff = lambda x, y = options.strike: max(x-y,0)
    elif options.opt_type is "put":
        payoff = lambda x, y = options.strike: max(y-x,0)

    option = Option(payoff, options.expiry)

    option_pricer = OptionPricer(option, options.drift, options.volatility, options.iter_num)

    print("The price of the given option is {}.".format(option_pricer.getPrice(options.spot)))