#!/usr/bin/env python

"""
Execute commands against a remote cluster

Cast is a utility for executing commands in parallel against a remote cluster
that arguably operates a little better than just 'run SSH in a loop.' But
that probably also means it has a higher potential for destroying all your
servers even faster. So, you know, mixed bag.

With no command specified, Cast will run interactively.
"""

import errno
import logging
import os
import sys
import optparse

from cast.optionParser import OptionParser

def main():

    usage = "%prog [options] command"
    parser = OptionParser(usage)

    (options, args) = parser.parse_args()
    print("Hello, world!")


if __name__ == '__main__':
    main()