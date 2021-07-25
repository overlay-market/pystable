import os
import subprocess


def libstable_path() -> str:
    '''Get path to libstable directory'''
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.abspath(os.path.join(path, os.pardir))
    return os.path.abspath(os.path.join(path, 'libstable'))


def make_libstable():
    '''Make libstable'''
    path = libstable_path()
    subprocess.run(['make'], cwd=path)


make_libstable()
