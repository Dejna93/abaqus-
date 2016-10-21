import os
from os.path import expanduser

attributes = [
    'PROJECT_PLUGIN'
    'PLUGIN_NAME'
    'ABAQUS_PLUGINS_DIR'
]

PROJECT_DIR = os.path.dirname(os.path.realpath(os.path.join(__file__, '../')))
PROJECT_PLUGIN = os.path.join(PROJECT_DIR, 'plugin')
USER_HOME_DIR = expanduser("~")
PLUGIN_NAME = "GoatSoft"
ABAQUS_PLUGINS_DIR = os.path.join(USER_HOME_DIR, os.path.join('abaqus_plugins', PLUGIN_NAME))

COPY_IGNORE_FILES = [
    '__init__.py',
    'README.md'
]