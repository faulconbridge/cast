import argparse

class SetConfig(argparse.Namespace):
    """Set Cast configuration values"""
    name = "set-config"
    usage = """
    %prog <command>"""
    summary = "Set Cast configuration variables"

    def __init__(self, args):
        data = vars(args)
        if data["workers"]:
            print(data["workers"])
        else:
            print("No workers :-(")
