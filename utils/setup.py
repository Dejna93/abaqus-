import importlib
import os
import shutil
from zipfile import ZipFile
import pip
from utils.settings import config, Config
import subprocess
import subprocess as sub

config = Config()

def install_libs_from_pip():
    try:
        pip.main(['install', '-r', config.REQUIREMENTS_FILE])
    except pip.PipError as e:
        print e
    finally:
        print "End!"
    pip.main(['install', 'nose'])


if __name__ == '__main__':
    install_libs_from_pip()