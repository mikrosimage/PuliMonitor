from pulimonitor.util.path import GENERAL_CONFIG_PATH
from ConfigParser import ConfigParser


def get(refresh=False):
    if refresh:
        get.config = None
    if get.config:
        return get.config
    get.config = Config()
    return get.config

get.config = None


class Config(ConfigParser, object):
    '''
    ConfigParser subclass that allows to conveniently access/write settings.
    '''

    def __init__(self):
        ConfigParser.__init__(self)
        self.read(GENERAL_CONFIG_PATH)

    def items(self, section, raw=False, vars=None):
        if section == "Servers":
            items = super(Config, self).items(section, raw, vars)
            servers = []
            for _, value in items:
                hostname, port = value.split(":")
                servers.append((hostname, int(port)))
            return servers
        return ConfigParser.items(self, section, raw=raw, vars=vars)


if __name__ == '__main__':
    c = Config()
