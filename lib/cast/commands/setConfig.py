import argparse
import configparser
from cast.defaults import config_path, write_defaults, DEFAULTS

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

    def validate_arguments(self, args):
        if (args.shortname or args.group or args.key) and not args.host:
            argparse.ArgumentParser().error("--host must be specified\n")
        if args.host and not args.key:
            argparse.ArgumentParser().error("--key must be specified if a host is provided\n")

    def set_workers(self, workers):
        config = configparser.ConfigParser()
        config.read(config_path())
        config["DEFAULTS"]["workers"] = str(workers)
        write_defaults(config)

        print("Changed default workers from {0} to {1}".format(
            getattr(DEFAULTS, "workers"), str(workers))
        )
        setattr(DEFAULTS, "workers", workers)
