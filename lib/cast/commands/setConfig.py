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
            self.set_host_entry(args.host, args.user, args.port,
                                args.shortname, args.group, args.key)

    def validate_arguments(self, args):
        if not args.workers and not args.host:
            argparse.ArgumentParser().error(
                "One of --workers or --host must be specified\n")

    def set_worker_entry(self, workers):
        print("Changed default workers from {0} to {1}".format(
            DEFAULTS.get_default("workers"), str(workers))
        )
        DEFAULTS.set_default("workers", workers)

    def set_host_entry(self, host, user, port, shortname, group, key):
        hostentry = {
            "host": host,
            "user": user,
            "port": port,
            "shortname": shortname,
            "group": group,
            "key": key
        }

        index = HOSTS.set_host(hostentry)

        if index > -1:
            action = ("updated", "in")
        else:
            action = ("added", "to")

        print("Successfully {0} Host \"{1}\" {2} the hostfile.".format(
            action[0], HOSTS.get_host("host", host)["host"], action[1])
        )
