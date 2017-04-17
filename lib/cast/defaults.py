import configparser
import os
import sys

def config_path():
    return os.path.abspath(os.path.expanduser("~/.castrc"))

def write_defaults(config):
    with open(config_path(), "w") as configfile:
        config.write(configfile)

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
        else:
            raise AttributeError(name)

DEFAULTS = Defaults(config_path())