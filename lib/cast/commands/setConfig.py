import argparse
import configparser
from cast.defaults import config_path, DEFAULTS

class SetConfig(argparse.Namespace):
    """Set Cast configuration values"""
    name = "set-config"
    usage = """
    %prog <command>"""
    summary = "Set Cast configuration variables"

    def __init__(self, args):
        self.validate_arguments(args)

        if args.workers:
            self.set_workers(args.workers)

        if args.host:
            self.set_host(args.host, args.shortname, args.group, args.key)

    def validate_arguments(self, args):
        if (args.shortname or args.group or args.key) and not args.host:
            argparse.ArgumentParser().error("--host must be specified\n")
        if args.host and not args.key:
            argparse.ArgumentParser().error("--key must be specified if a host is provided\n")

    def set_workers(self, workers):
        print("Changed default workers from {0} to {1}".format(
            getattr(DEFAULTS, "workers"), str(workers))
        )
        setattr(DEFAULTS, "workers", workers)

    def set_host(self, host, shortname, group, key):
        config = configparser.ConfigParser()
        config.read(config_path())
        config["HOSTS"]["host"]
        print(config.__class__)
        print(config["DEFAULTS"].__class__)
