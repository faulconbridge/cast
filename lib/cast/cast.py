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
from cast.commands.getConfig import GetConfig
from cast.commands.deleteConfig import DeleteConfig

def set_config_arguments(self):
    self.add_argument(
        "--workers",
        dest = "workers",
        type = int,
        help = "The maximum number of ssh workers to spawn"
    )

    self.add_argument(
        "--host",
        dest = "host",
        help = "Specify the canonical URL of the host to connect to"
    )

    self.add_argument(
        "--user",
        dest = "user",
        default = getpass.getuser(),
        help = "Specify the user to connect as. Defaults to your current username"
    )

    self.add_argument(
        "--port",
        dest = "port",
        type = int,
        default = 22,
        help = "Specify the port, if non-standard. Defaults to port 22"
    )

    self.add_argument(
        "--shortname",
        dest = "shortname",
        help = "Specify the (human-readable) shortname of the host"
    )

    self.add_argument(
        "--group",
        dest = "group",
        help = "Specify a cluster group for easier management"
    )

    self.add_argument(
        "--key",
        dest = "key",
        default = "~/.ssh/id_rsa",
        help = """
            Specify the location on disk of the SSH private key
            used to connect to the host. Defaults to ~/.ssh/id_rsa
        """
    )

    return self

def get_or_del_config_arguments(self):
    self.add_argument(
        "--host",
        dest = "host",
        help = "Specify the canonical URL of the host you are looking up"
    )

    self.add_argument(
        "--workers",
        dest = "workers",
        action = "store_true",
        help = "Returns the maximum number of workers spawned"
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
    set_config = set_config_arguments(set_config)
    set_config.set_defaults(func = SetConfig)

    get_config = subparsers.add_parser("get-config")
    get_config = get_or_del_config_arguments(get_config)
    get_config.add_argument(
        "--list-all-hosts",
        dest = "all_hosts",
        action = "store_true",
        help = "List all hosts currently registered with Cast"
    )
    get_config.set_defaults(func = GetConfig)

    delete_config = subparsers.add_parser("delete-config")
    delete_config = get_or_del_config_arguments(delete_config)
    delete_config.set_defaults(func = DeleteConfig)

    args = parser.parse_args()

    try:
        args.func(args)
    except AttributeError:
        parser.parse_args(["-h"])

    print("Hello, world!")

if __name__ == "__main__":
    main()
