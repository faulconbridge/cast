import argparse
from cast.commands.setConfig import setConfig

class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, usage, **kwargs):
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

        set_config = subparsers.add_parser('set-config')
        set_config.add_argument(
            "--host",
            dest = "host",
            required = True,
            help = "Specify the canonical URL of the host to connect to"
        )

        set_config.add_argument(
            "--shortname",
            dest = "shortname",
            help = "Specify the (human-readable) shortname of the host"
        )

        set_config.add_argument(
            "--key",
            dest = "key",
            help = """
                Specify the location on disk of the SSH private key
                used to connect to the host
            """
        )
        set_config.set_defaults(func = setConfig)
