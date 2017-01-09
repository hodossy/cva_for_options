# cva_for_options
Approximates the CVA for option contracts

# Install

Go to where the setup.py is, and call

    python setup.py install --user
    
Order of installation:

1. brownian_motion
2. option_pricer
3. cva_for_options

# Usage

brownian_motion can only be used in python scripts, while option_pricer and cva_for_options has a command line interface. For detailed instructions call

    python option_pricer --help
    python cva_for_options --help
