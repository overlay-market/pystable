import platform
import os

LIBSTABLE_PATH_ARCH = 'pystable/_extensions/arch/libstable.so'
LIBSTABLE_PATH_OSX_ARM = 'pystable/_extensions/osx-arm/libstable.so'
LIBSTABLE_PATH_OSX_INTEL = 'pystable/_extensions/osx-intel/libstable.so'
LIBSTABLE_PATH_UBUNTU = 'pystable/_extensions/ubuntu/libstable.so'


def libstable_path(libstable_path=None) -> str:
    '''Get path to libstable.so'''
    if libstable_path is None:
        platform_id = platform.platform()
        if "arch" in platform_id:
            # Linux-5.12.14-arch1-1-x86_64-with-glibc2.33
            libstable_path = LIBSTABLE_PATH_ARCH
        elif "aws" in platform_id:
            # Linux-5.4.0-1045-aws-x86_64-with-glibc2.31
            libstable_path = LIBSTABLE_PATH_UBUNTU
        elif "arm" in platform_id:
            # macOS-11.4-arm64-arm-64bit
            libstable_path = LIBSTABLE_PATH_OSX_ARM
        elif "x86" in platform_id:
            # macOS-10.15.7-x86_64-i386-64bit
            libstable_path = LIBSTABLE_PATH_OSX_INTEL
        else:
            print('OS not supported. Please use Arch Linux, Ubuntu, or OSX')

    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.abspath(os.path.join(path, os.pardir))
    return os.path.abspath(os.path.join(path, libstable_path))
