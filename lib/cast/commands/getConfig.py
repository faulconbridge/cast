import argparse
import configparser
from cast.defaults import config_path, DEFAULTS, HOSTS

class GetConfig(argparse.Namespace):
    """Set Cast configuration values"""
    name = "get-config"
    usage = "%prog <command>"
    summary = "Retrieve Cast configuration variables"

    def __init__(self, args):
        self.validate_arguments(args)

        if args.workers:
            self.get_worker_entry(args.workers)

        if args.host:
            self.get_host_entry(args.host)

        if args.all_hosts:
            self.get_all_hosts()

    def validate_arguments(self, args):
        if not (args.host or args.workers or args.all_hosts):
            argparse.ArgumentParser().error(
                "One of --workers or --host must be specified\n")

    def get_worker_entry(self, workers):
        print("We will spawn up to {0} workers".format(
            DEFAULTS.get_default("workers"))
        )

    def get_host_entry(self, host):
        hostinfo = HOSTS.get_host("host", host)
        print(
            "     Host: {0}\n".format(hostinfo["host"]),
            "     User: {0}\n".format(hostinfo["user"]),
            "     Port: {0}\n".format(hostinfo["port"]),
            "    Group: {0}\n".format(hostinfo["group"]),
            "Shortname: {0}\n".format(hostinfo["shortname"]),
            "  Keyfile: {0}".format(hostinfo["key"]))

    def get_all_hosts(self):
        for host in HOSTS._HOSTS:
            print(
                "     Host: {0}\n".format(host["host"]),
                "     User: {0}\n".format(host["user"]),
                "     Port: {0}\n".format(host["port"]),
                "    Group: {0}\n".format(host["group"]),
                "Shortname: {0}\n".format(host["shortname"]),
                "  Keyfile: {0}".format(host["key"]))
