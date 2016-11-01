import errno
import getopt
import os
import shutil
import sys
import settings as config


class MoverClass(object):
    def __init__(self, *args, **kwargs):
        pass

    def copy_files_from_abaqus(self, destiny_dir):
        print(os.path.isdir(os.path.join(config.PROJECT_DIRO), destiny_dir))

    def copy_files_to_abaqus(self, from_dir, flat=False):
        files = check_dir(from_dir)
        if not os.path.isdir(config.ABAQUS_PLUGINS_DIR):
            os.mkdir(config.ABAQUS_PLUGINS_DIR)
        self.clean_files(config.ABAQUS_PLUGINS_DIR)

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

    def clean_files(self, destinity_dir):
        files = check_dir(destinity_dir)
        for file in files:
            file_name = os.path.join(config.ABAQUS_PLUGINS_DIR, file)
            os.remove(file_name)


def check_dir(dir):
    """Checking if dir is not empty"""
    if not os.path.isdir(dir):
        raise IOError(u"This is not a directory")
    try:
        files = os.listdir(dir)
    except IOError as e:
        print u"You can't copy file", e
    except WindowsError as e:
        print u"You can't copy empty dir, %s", e
    else:
        return files


def main(*args, **kwargs):
    mover = MoverClass(*args, **kwargs)
    mover.copy_files_to_abaqus(config.PROJECT_PLUGIN, flat=False)


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:e:f:", ["import", "export", "flat"])
    except getopt.GetoptError as e:
        print(u"Some errors: ", e)
        sys.exit(2)

    operation = ""
    args = []

    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--import"):
            operation = arg
        elif opt in ("-o", "--export"):
            operation = arg
        elif opt in ("-f", "--flat"):
            args.append(arg)
    args.append(operation)

    main(args)
