import errno
import shutil

import sys
from settings import *

def copy_files(from_dir):
    try:
        files = os.listdir(from_dir)
        print('file_dir', files)
    except IOError as e:
        print (u"You can't coppy empty dir, %s", e)

    for file in files:
        file_name = os.path.join(from_dir, file)
        if os.path.isfile(file_name) and file not in COPY_IGNORE_FILES:
            shutil.copy(file_name, ABAQUS_PLUGINS_DIR)
        elif os.path.isdir(file_name):
            copy_files(file_name)


def clean_files():
    try:
        files = os.listdir(ABAQUS_PLUGINS_DIR)
    except IOError as e:
        print (u"This Dir is empty, %s", e)
    for file in files:
        file_name = os.path.join(ABAQUS_PLUGINS_DIR, file)
        os.remove(file_name)


def main(argv):
    args = dict(arg.split('=') for arg in argv)
    clean_files()
    copy_files(PROJECT_PLUGIN)

if __name__ == '__main__':
    main(sys.argv[1:])
