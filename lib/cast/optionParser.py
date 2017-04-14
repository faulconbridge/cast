import optparse

class Option(optparse.Option):
    TYPES = optparse.Option.TYPES
    TYPE_CHECKER = optparse.Option.TYPE_CHECKER


class OptionParser(optparse.OptionParser):
    def __init__(self, usage, **kwargs):
        optparse.OptionParser.__init__(
            self,
            usage,
            option_class=Option,
            **kwargs
        )

        self.disable_interspersed_args()
        # self.add_option(
        #     "-h",
        #     "--help",
        #     dest="help",
        #     action="help",
        #     help="Show help."
        # )

        self.add_option(
            "-v",
            "--verbose",
            dest="verbose",
            action="count",
            default=0,
            help="Provide additional output"
        )

        self.add_option(
            "-V",
            "--version",
            dest="version",
            action="store_true",
            help="Display version information"
        )