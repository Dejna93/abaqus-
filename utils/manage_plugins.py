import errno
import getopt
import os
import shutil
import sys
import subprocess as sub
from settings import config
import pip
import importlib
from zipfile import ZipFile, error as zfError
import threading
import Tkinter as tk


class AbaqusInstalator(object):
    def __init__(self):
        pass

    def create_installer(self):
        """Method pack and install plugin"""

    def collect_libs(self):
        """The method download libs with their dependecies and zipped in dir"""
        for package in config.INSTALLED_LIBS:
            try:
                pip.main(['download', '-d', config.LIBS_BUNDLE, package])
            except pip.PipError as e:
                print u"Error hen package '%s' was installing \n Error: %s" % (package, e)
        zf = ZipFile(os.path.join(config.PROJECT_DIR, 'zipped_libs.zip'), mode='w')
        for f in os.listdir(config.LIBS_BUNDLE):
            path = os.path.join(config.LIBS_BUNDLE, f)
            lenDirPath = len(config.LIBS_BUNDLE)
            try:
                zf.write(path, path[lenDirPath:])
            except zfError as e:
                print u"Something went wrong with creating zip. \n Error: %s" % e
        zf.close()

        try:
            shutil.rmtree(config.LIBS_BUNDLE)
        except shutil.Error as e:
            print u"Some errors with removing libs_bundle. \n Error: %s" % e

    def create_requirements_file(self):
        p = sub.Popen(['pip', 'freeze'], stdout=sub.PIPE, stderr=sub.PIPE)
        output, errors = p.communicate()
        return output, errors

    def copy_files(self, source, destiny, flat, ignore_files=['']):
        """
        The method will copy files from source dir to destiny dir
        Source: dir with source files
        Destiny: dir where we copy source files
        ignore_files: list of file names which will be ignored
        flat: copy not-tree just all files in main dir
        """
        files = self.get_files(source)

        if flat:
            if not os.path.isdir(config.ABAQUS_PLUGINS_DIR):
                os.mkdir(config.ABAQUS_PLUGINS_DIR)

            for file in files:
                file_name = os.path.join(source, file)
                if os.path.isfile(file_name) and file not in config.COPY_IGNORE_FILES:
                    shutil.copy(file_name, config.ABAQUS_PLUGINS_DIR)
                elif os.path.isdir(file_name):
                    self.copy_files(file_name, destiny, flat)
        else:
            ignore_files = shutil.ignore_patterns(' '.join(ignore_files))
            if os.path.exists(config.ABAQUS_PLUGINS_DIR):
                shutil.rmtree(config.ABAQUS_PLUGINS_DIR)
                shutil.copytree(source, config.ABAQUS_PLUGINS_DIR, ignore=ignore_files)
            else:
                shutil.copytree(source, config.ABAQUS_PLUGINS_DIR, ignore=ignore_files)

    def get_files(self, dir):
        """The method will check if dir is no empty and return list of files"""
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

    def install_libs(self, requirements=None, destiny_path=None):
        """Wraper for pip install"""
        # if not requirements and not destiny_path:
        #     raise u"InstallLibsError \n requirements and destiny_path can't be empty "
        try:
            pip.main(['install', '--upgrade pip', 'pip'])
        except pip.PipError as e:
            print e
        if destiny_path:
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

    def libs_install_test(self):
        with open(config.REQUIREMENTS_FILE) as file:
            for lib in file:
                command = '-m pip install %s'%lib
                output, errors = self.python_command(command)
                yield output, errors, lib

    def python_command(self, text):
        app = 'python.exe'
        appPath = os.path.join(config.ABAQUS_PYTHON, app)
        command = [appPath]
        command.extend(text.split())
        try:
            p = sub.Popen(command, stdout=sub.PIPE, stderr=sub.PIPE)
            p_status = p.wait()
        except sub.CalledProcessError as e:
            print e
        finally:
            output, errors = p.communicate()
            return output, errors

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:i:c:d", ["flat", 'install', 'copy', 'destiny'])
    except getopt.GetoptError as e:
        print u"Some errors: %s" % e
        sys.exit(2)

    kwargs = {'flat': False}

    for opt, arg in opts:
        if opt == '-h':
            print '-c --copy copy <from_dir> -d --destiny <to_dir> \n' \
                  '-f --flat copy not-tree, it will copy all files into main dir \n' \
                  '-l --libs collect all libs used in your plugin \n' \
                  '-i --install install your plugin into abaqus \n'
            sys.exit()
        elif opt in ("-f", "--flat"):
            kwargs['flat'] = True