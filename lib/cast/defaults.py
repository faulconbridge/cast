import configparser
import json
import os
import sys

def config_path(path):
    return os.path.abspath(os.path.expanduser(path))


class Defaults(object):
    _DEFAULTS = {
        "workers": 4
    }

    _DEFAULTS_CONVERTERS = {
        "workers": configparser.ConfigParser.getint
    }

    def __init__(self, filename):
        config = configparser.ConfigParser()
        parsed = config.read(filename)

        if parsed:
            self._parse_config(config)

    def _parse_config(self, config):
        for key, val in self._DEFAULTS_CONVERTERS.items():
            try:
                self._DEFAULTS[key] = val(config, 'DEFAULTS', key)
            except:
                pass

    def __getattr__(self, name):
        if name in self._DEFAULTS:
            return self._DEFAULTS[name]
        else:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        if name in self._DEFAULTS:
            self._DEFAULTS[name] = value

            config = configparser.ConfigParser()
            config["DEFAULT"] = {}

            for key, val in self._DEFAULTS.items():
                config["DEFAULT"]["{}".format(key)] = str(val)

            with open(config_path("~/.castrc"), "w") as configfile:
                config.write(configfile)
        else:
            raise AttributeError(name)

DEFAULTS = Defaults(config_path("~/.castrc"))