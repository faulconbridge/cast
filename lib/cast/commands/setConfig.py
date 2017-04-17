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
        data = vars(args)

        if data["workers"]:
            config = configparser.ConfigParser()
            config.read(config_path())
            config["DEFAULTS"]["workers"] = str(data["workers"])
            write_defaults(config)

            print("Changed default workers from {} to {}".format(
                getattr(DEFAULTS, "workers"), str(data["workers"]))
            )
            setattr(DEFAULTS, "workers", data["workers"])
        else:
            print("No workers to change :-(")
