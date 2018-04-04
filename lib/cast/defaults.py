import configparser
import json
import os
import sys

def config_path(path, filename):
    """Make things less funky, primarily on Windows machines"""
    return os.path.abspath(os.path.expanduser(path) + "/" + filename)

class HostException(Exception):
    def __init__(self, key, value):
        print(
            "Hmm...We couldn't find the record ({0}: {1})",
            "you were looking for.\nCheck that you spelled",
            "everything correctly and try again?".format(key, value))

        sys.exit(0)

class Defaults(object):
    """Global defaults that impact how Cast operates.

    Currently, it's just the maximum number of workers
    allowed to be spawned concurrently, but I expect this
    number will increase as I make things less terrible.
    """
    _DEFAULTS = {
        "workers": 4
    }

    _DEFAULTS_CONVERTERS = {
        "workers": configparser.ConfigParser.getint
    }

    def __init__(self, filename):
        self._defaults = self._DEFAULTS.copy()
        config = configparser.ConfigParser()
        parsed = config.read(filename)

        if parsed:
            self._parse_config(config)

    def _parse_config(self, config):
        """Convert the INI-style config file to a
        less awful dict
        """
        for key, val in self._DEFAULTS_CONVERTERS.items():
            try:
                self._defaults[key] = val(config, 'DEFAULTS', key)
            except:
                pass

    def get_default(self, name):
        if name in self._defaults:
            return self._defaults[name]
        else:
            raise AttributeError(name)

    def set_default(self, name, value):
        if name in self._defaults:
            self._defaults[name] = value

            config = configparser.ConfigParser()
            config["DEFAULTS"] = {}

            for key, val in self._defaults.items():
                config["DEFAULTS"]["{}".format(key)] = str(val)

            with open(config_path("~/", ".castrc"), "w") as configfile:
                config.write(configfile)
        else:
            raise AttributeError(name)

    def delete_default(self, name):
        if name in self._defaults:
            self.set_default(name, self._DEFAULTS[name])
        else:
            raise AttributeError(name)

class Hosts(object):
    """Any remote nodes that the user has specified
    locally will be registered here as a list of dicts.

    There's almost certainly A Better Way (tm), but I
    don't know Python, so this is what we're going with
    for now.
    """
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
        index = self.exists(key, value)
        if index > -1:
            return self._HOSTS[index]
        else:
            raise HostException(key, value)

    def set_host(self, value):
        """Updates an existing host record, if found, or
        creates a new one and appends to both the global
        environment and to the hosts config file.

        Right now this will overwrite completely any existing
        record if a match is found, so you can't, for example,
        do something like

        cast set-config --host test --key ~/.ssh/new_key_rsa

        without wiping out user/port/shortname/group.

        This should probably be fixed at some point, but for
        now I can get away with calling it a "feature".
        """
        index = self.exists("host", value["host"])

        if index > -1:
            self._HOSTS[index] = value
        else:
            self._HOSTS.append(value)

        with open(config_path("~/.cast", "hosts.json"), "w") as configfile:
            json.dump(self._HOSTS, configfile)

        return index

    def delete_host(self, host):
        index = HOSTS.exists("host", host)
        if index == -1:
            raise HostException("host", host)

        dropped = self._HOSTS.pop(index)

        with open(config_path("~/.cast", "hosts.json"), "w") as configfile:
            json.dump(self._HOSTS, configfile)

        return dropped

    def exists(self, key, value):
        """Iterates through the list of hosts to identify
        the index of a host if it already exists. Returns
        -1 if the record could not be found.
        """
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
