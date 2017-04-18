import configparser
import json
import os
import sys

def config_path(path, filename):
    return os.path.abspath(os.path.expanduser(path) + "/" + filename)


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

    def get_default(self, name):
        if name in self._DEFAULTS:
            return self._DEFAULTS[name]
        else:
            raise AttributeError(name)

    def set_default(self, name, value):
        if name in self._DEFAULTS:
            self._DEFAULTS[name] = value

            config = configparser.ConfigParser()
            config["DEFAULT"] = {}

            for key, val in self._DEFAULTS.items():
                config["DEFAULT"]["{}".format(key)] = str(val)

            with open(config_path("~/", ".castrc"), "w") as configfile:
                config.write(configfile)
        else:
            raise AttributeError(name)

class Hosts(object):
    _HOSTS = {}

    def __init__(self, path, filename):
        path = os.path.abspath(os.path.expanduser(path))
        if not os.path.exists(path):
            os.makedirs(path)

        with open(config_path(path, filename), "r+") as f:
            try:
                self._HOSTS = json.load(f)
            except (ValueError, json.decoder.JSONDecodeError):
                self._HOSTS = json.loads('[]')

    def get_host(self, key, value):
        index = exists(self._HOSTS, key, value)
        if index > -1:
            return self._HOSTS[index]
        else:
            raise AttributeError(host)

    def set_host(self, value):
        index = self.exists("host", value["host"])

        if index > -1:
            self._HOSTS[index] = value
            print("updated")
        else:
            self._HOSTS.append(value)
            print("appended")

        with open(config_path("~/.cast", "hosts.json"), "w") as configfile:
            json.dump(self._HOSTS, configfile)

    def exists(self, key, value):
        for idx, host in enumerate(self._HOSTS):
            if host[key] == value:
                index = idx
        try:
            index
        except:
            index = -1

        return index

DEFAULTS = Defaults(config_path("~/", ".castrc"))
HOSTS = Hosts("~/.cast/", "hosts.json")
