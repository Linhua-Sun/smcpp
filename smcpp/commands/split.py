'Fit SMC++ to data using the EM algorithm'
from __future__ import absolute_import, division, print_function
import argparse
import numpy as np
import scipy.optimize
import pprint
import sys
import itertools
import sys
import time
import os
import json

# Package imports
from ..logging import getLogger, setup_logging
from ..analysis import SplitAnalysis
from .estimate import add_common_estimation_args

logger = getLogger(__name__)
np.set_printoptions(linewidth=120, suppress=True)

def init_parser(parser):
    '''Configure parser and parse args.'''
    add_common_estimation_args(parser)
    parser.add_argument('pop1', help="marginal fit for population 1")
    parser.add_argument('pop2', help="marginal fit for population 2")
    parser.add_argument('data', nargs="+", help="data file(s) in SMC++ format")


def main(args):
    ## Create output directory
    try:
        os.makedirs(args.outdir)
    except OSError:
        pass  # directory exists

    ## Initialize the logger
    setup_logging(args.verbose, os.path.join(args.outdir, ".debug.txt"))

    ## Save all the command line args and stuff
    logger.debug(sys.argv)
    logger.debug(args)

    ## Fill in some of the population-genetic parameters from previous model run
    ## TODO ensure that these params agree in both models?
    d = json.load(open(args.pop1, "rt"))
    args.N0 = d['N0']
    args.theta = d['theta']
    args.rho = None

    ## Construct analysis
    analysis = SplitAnalysis(args.data, args)
    analysis.run()
