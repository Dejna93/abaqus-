import errno
import getopt
import os
import shutil
import sys
from settings import config
from distutils.sysconfig import get_python_lib
from pip._vendor import pkg_resources
import re

class MoverClass(object):
    def __init__(self, *args, **kwargs):
        super(MoverClass)

    def clean_files(self, destinity_dir):
        shutil.rmtree(destinity_dir)

    def copy_files_to_abaqus(self, from_dir, flat=False):
        files = check_dir(from_dir)
        self.clean_files(config.ABAQUS_PLUGINS_DIR)
        if not os.path.isdir(config.ABAQUS_PLUGINS_DIR):
            os.mkdir(config.ABAQUS_PLUGINS_DIR)
        if flat:
            for file in files:
                file_name = os.path.join(from_dir, file)
                if os.path.isfile(file_name) and file not in config.COPY_IGNORE_FILES:
                    shutil.copy(file_name, config.ABAQUS_PLUGINS_DIR)
                elif os.path.isdir(file_name):
                    self.copy_files_to_abaqus(file_name)
        else:
            ignore_files = shutil.ignore_patterns(' '.join(config.COPY_IGNORE_FILES))
            if os.path.exists(config.ABAQUS_PLUGINS_DIR):
                shutil.rmtree(config.ABAQUS_PLUGINS_DIR)
                shutil.copytree(from_dir, config.ABAQUS_PLUGINS_DIR, ignore=ignore_files)


class InstallLibsInAbaqus(object):

    def copy_libs(self):


    def install_libs(self):
        paths = self.find_dependencies()
        print(os.listdir(os.path.join(get_python_lib())))
        print "dep", paths
        for lib in paths:
            for file in os.listdir(os.path.join(get_python_lib())):
                if file in paths:
                    print'Mamy go:', file
                    print u'A to sciezka', os.path.join(get_python_lib(), lib)

    def find_dependencies(self):
        dependencies = []
        for lib in config.INSTALLED_LIBS:
            _package = pkg_resources.working_set.by_key[lib]
            dependencies.append(lib)
            for dependence in _package.requires():
                dependencies.append(re.split(r'[!<>=]', str(dependence))[0])
        return dependencies


def check_dir(dir):
    """Checking if dir is not empty"""
    if not os.path.isdir(dir):
        raise IOError(u"This is not a directory")
    try:
        files = os.listdir(dir)
    except IOError as e:
        print u"You can't copy file: %s" % e
    except WindowsError as e:
        print u"You can't copy empty dir, %s" % e
    else:
        return files


def main(*args, **kwargs):
    # mover = MoverClass(*args, **kwargs)
    # mover.copy_files_to_abaqus(config.PROJECT_PLUGIN, flat=kwargs['flat'])
    liberator = InstallLibsInAbaqus()
    liberator.install_libs()

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hfm:", ["flat", 'maindir'])
    except getopt.GetoptError as e:
        print u"Some errors: %s" % e
        sys.exit(2)

    kwargs = {'flat': False}

    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-f", "--flat"):
            kwargs['flat'] = True

    main(**kwargs)
