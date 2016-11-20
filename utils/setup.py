import importlib
import os
import shutil
from zipfile import ZipFile
import pip
from utils.settings import config
import subprocess


class SetUp(object):
    def install_libs_from_local(self, requirements=None, destiny_path=None):
        """Wraper for pip install"""
        try:
            pip.main(['install', '--upgrade pip', 'pip'])
        except pip.PipError as e:
            print e
        zf = ZipFile(os.path.join(config.PROJECT_DIR, 'zipped_libs.zip'))
        zf.extractall(config.LIBS_BUNDLE)
        zf.close()
        requirements = os.listdir(destiny_path)
        for i in range(len(requirements)):
            requirements[i] = os.path.join(destiny_path, requirements[i])

        for package in requirements:
            try:
                importlib.import_module(package)
            except ImportError:
                pip.main(['install', package])

        if os.path.exists(config.LIBS_BUNDLE):
            try:
                shutil.rmtree(config.LIBS_BUNDLE)
            except shutil.Error as e:
                print u"Some errors with removing libs_bundle. \n Error: %s" % e
