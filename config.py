import configparser

CONFIG_FILE = 'config.ini'


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Config(object):
    __metaclass__ = Singleton

    def __init__(self, ini_file=CONFIG_FILE):
        config = configparser.ConfigParser()
        config.read(ini_file, 'UTF-8')

        boss_name = dict(config.items('clan_battle_boss_name'))
        self.cfg = {
            'clan_battle_boss_name': tuple([boss_name['1'],
                                            boss_name['2'],
                                            boss_name['3'],
                                            boss_name['4'],
                                            boss_name['5']])
        }

    def get(self, key):
        return self.cfg[key]
