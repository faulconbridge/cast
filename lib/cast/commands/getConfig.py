import argparse
import configparser
from cast.defaults import config_path, DEFAULTS, HOSTS

class GetConfig(argparse.Namespace):
    """Set Cast configuration values"""
    name = "get-config"
    usage = """
    %prog <command>"""
    summary = "Retrieve Cast configuration variables"

    def __init__(self, args):
        self.validate_arguments(args)

        if args.workers:
            self.get_worker_entry(args.workers)

        if args.host:
            self.get_host_entry(args.host)

    def validate_arguments(self, args):
        if not (args.host or args.workers):
            argparse.ArgumentParser().error("One of --workers or --host must be specified\n")

    def get_worker_entry(self, workers):
        print("We will spawn up to {0} workers".format(
            DEFAULTS.get_default("workers"))
        )

    def get_host_entry(self, host):
        hostinfo = HOSTS.get_host("host", host)
        print("""     Host: {0}
     User: {1}
     Port: {2}
    Group: {3}
Shortname: {4}
  Keyfile: {5}""".format(hostinfo["host"],
                         hostinfo["user"],
                         hostinfo["port"],
                         hostinfo["group"],
                         hostinfo["shortname"],
                         hostinfo["key"])
        )
