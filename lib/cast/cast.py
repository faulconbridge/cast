#!/usr/bin/env python

"""
Execute commands against a remote cluster

Cast is a utility for executing commands in parallel against a remote cluster
that arguably operates a little better than just "run SSH in a loop." But
that probably also means it has a higher potential for destroying all your
servers even faster. So, you know, mixed bag.
"""

import errno
import logging
import os
import sys
import argparse
import getpass

from cast.commands.setConfig import SetConfig

def set_general_config_arguments(self):
    self.add_argument(
        "--workers",
        dest = "workers",
        type = int,
        help = "The maximum number of ssh workers to spawn"
    )

    return self

def set_host_config_arguments(self):
    self.add_argument(
        "--host",
        dest = "host",
        help = "Specify the canonical URL of the host to connect to"
    )

    self.add_argument(
        "--user",
        dest = "user",
        default = getpass.getuser(),
        help = "Specify the user to connect as. Defaults to your current username."
    )

    self.add_argument(
        "--port",
        dest = "port",
        default = 22,
        help = "Specify the port, if non-standard. Defaults to port 22."
    )

    self.add_argument(
        "--group",
        dest = "group",
        help = "Specify a cluster group for easier management"
    )

    self.add_argument(
        "--shortname",
        dest = "shortname",
        help = "Specify the (human-readable) shortname of the host"
    )

    self.add_argument(
        "--key",
        dest = "key",
        help = """
            Specify the location on disk of the SSH private key
            used to connect to the host
        """
    )

    return self

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--verbose",
        dest = "verbose",
        action = "count",
        default = 0,
        help = "Provide additional output"
    )

    parser.add_argument(
        "-V",
        "--version",
        dest = "version",
        action = "store_true",
        help = "Display version information"
    )

    subparsers = parser.add_subparsers(help = "Sub-command help")

    set_config = subparsers.add_parser("set-config")
    set_config = set_general_config_arguments(set_config)
    set_config = set_host_config_arguments(set_config)
    set_config.set_defaults(func = SetConfig)

    args = parser.parse_args()

    try:
        args.func(args)
    except:
        parser.parse_args(["-h"])

    print("Hello, world!")

if __name__ == "__main__":
    main()
