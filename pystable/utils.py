import os

LIBSTABLE_PATH = 'pystable/_extensions/libstable.so'


def libstable_path(libstable_path=LIBSTABLE_PATH) -> str:
    '''Get path to libstable.so'''
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.abspath(os.path.join(path, os.pardir))
    return os.path.abspath(os.path.join(path, libstable_path))
