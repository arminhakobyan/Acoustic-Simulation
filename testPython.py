from os import path
import errno
import os
from os import environ
import sys


ERROR_INVALID_NAME = 123

def is_pathname_valid(pathname: str) -> bool:
    '''
    `True` if the passed pathname is a valid pathname for the current OS;
    `False` otherwise.
    '''

    print('in is_pathname_valid')

    try:
        if not isinstance(pathname, str) or not pathname:
            return False

        _, pathname = path.splitdrive(pathname)
        root_dirname = environ.get('HOMEDRIVE', 'C:') \
            if sys.platform == 'win32' else sep
        assert path.isdir(root_dirname)

        root_dirname = root_dirname.rstrip(path.sep) + path.sep

        for pathname_part in pathname.split(path.sep):
            try:
                os.lstat(root_dirname + pathname_part)

            except OSError as exc:
                if hasattr(exc, 'winerror'):
                    if exc.winerror == ERROR_INVALID_NAME:
                        return False
                elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                    return False

    except TypeError as exc:
        return False
    else:
        return True

def is_path_creatable(pathname: str) -> bool:
    '''
    `True` if the current user has sufficient permissions to create the passed
    pathname; `False` otherwise.
    '''
    dirname = os.path.dirname(pathname) or os.getcwd()
    return os.access(dirname, os.W_OK)

def is_path_exists_or_creatable(pathname: str) -> bool:
    '''
    `True` if the passed pathname is a valid pathname for the current OS _and_
    either currently exists or is hypothetically creatable; `False` otherwise.

    This function is guaranteed to _never_ raise exceptions.
    '''
    try:
        return is_pathname_valid(pathname) and (
            os.path.exists(pathname) or is_path_creatable(pathname))
    except OSError:
        return False

p = 'Armine\\Lilit'

try:
    if not path.exists(path.dirname(p)):
        print('makedir path')
        os.makedirs(path.dirname(p))
except OSError:
    print('not valid pathname')