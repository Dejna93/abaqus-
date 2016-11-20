import fnmatch
import os
from os.path import expanduser


class Config(object):
    def __init__(self):

        self.PROJECT_DIR = os.path.dirname(os.path.realpath(os.path.join(__file__, '../')))
        self.PROJECT_PLUGIN = os.path.join(self.PROJECT_DIR, 'plugin')
        self.USER_HOME_DIR = expanduser("~")
        self.ABAQUS_PLUGINS_DIR = os.path.join(self.USER_HOME_DIR, os.path.join('abaqus_plugins', 'GoatSoft'))
        self.ABAQUS_LIBS_DIR = os.path.join(self.USER_HOME_DIR, os.path.join('abaqus_plugins', 'GoatSoft'))
        self.CONFIG_PATH = os.path.join('.', os.path.join('docs', 'config.txt'))
        self.LIBS_BUNDLE = os.path.join(self.PROJECT_DIR, 'libs_bundle')
        self.ABAQUS_DIR = 'C:\\SIMULIA\\Abaqus'

        for key, value in self.read_from_file().items():
            self.__dict__[key] = value

        self.COPY_IGNORE_FILES = [
            '__init__.py',
            'README.md'
        ]
        self.ABAQUS_LIBS_DIR = os.path.abspath(self.ABAQUS_LIBS_DIR)
        self.INSTALLED_LIBS = [
            'matplotlib',
        ]

    def read_from_file(self):
        config = {}
        with open(self.CONFIG_PATH, 'r') as file:
            for line in file:
                key, value = line.split("=")
                config[key] = value[:-1]
        return config

config = Config()