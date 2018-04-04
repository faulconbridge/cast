import argparse
import configparser
from cast.defaults import config_path, DEFAULTS, HOSTS

class DeleteConfig(argparse.Namespace):
    """Set Cast configuration values"""
    name = "delete-config"
    usage = "%prog <command>"
    summary = "Delete Cast configuration variables"

    def __init__(self, args):
        self.validate_arguments(args)

        if args.workers:
            self.delete_worker_entry(args.workers)

        if args.host:
            self.delete_host_entry(args.host)

    def validate_arguments(self, args):
        if not args.workers and not args.host:
            argparse.ArgumentParser().error(
                "One of --workers or --host must be specified\n")

    def delete_worker_entry(self, workers):
        print(
            "Changed default workers from {0} to system default {1}".format(
                DEFAULTS.get_default("workers"), 4))
        DEFAULTS.delete_default("workers")

    def delete_host_entry(self, host):
        dropped = HOSTS.delete_host(host)
        print(
            "Successfully dropped entry\n",
            "     Host: {0}\n".format(dropped["host"]),
            "     User: {0}\n".format(dropped["user"]),
            "     Port: {0}\n".format(dropped["port"]),
            "    Group: {0}\n".format(dropped["group"]),
            "Shortname: {0}\n".format(dropped["shortname"]),
            "  Keyfile: {0}".format(dropped["key"]))
