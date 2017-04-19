import argparse
import configparser
from cast.defaults import config_path, DEFAULTS, HOSTS

class SetConfig(argparse.Namespace):
    """Set Cast configuration values"""
    name = "set-config"
    usage = """
    %prog <command>"""
    summary = "Set Cast configuration variables"

    def __init__(self, args):
        self.validate_arguments(args)

        if args.workers:
            self.set_worker_entry(args.workers)

        if args.host:
            self.set_host_entry(args.host, args.shortname, args.group, args.key)

    def validate_arguments(self, args):
        if (args.shortname or args.group or args.key) and not args.host:
            argparse.ArgumentParser().error("--host must be specified\n")
        if args.host and not args.key:
            argparse.ArgumentParser().error("--key must be specified if a host is provided\n")

    def set_worker_entry(self, workers):
        print("Changed default workers from {0} to {1}".format(
            DEFAULTS.get_default("workers"), str(workers))
        )
        DEFAULTS.set_default("workers", workers)

    def set_host_entry(self, host, shortname, group, key):
        hostentry = {
            "host": host,
            "shortname": shortname,
            "group": group,
            "key": key
        }

        HOSTS.set_host(hostentry)

        print("Successfully added {} to the hostfile.".format(HOSTS.get_host("host", host)))
