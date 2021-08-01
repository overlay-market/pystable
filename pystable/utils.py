import platform
import os

BASE = 'pystable/_extensions/'
PATH_LINUX_GLIBC_2_31 = '{}linux/gclib-2-31/libstable.so'.format(BASE)
PATH_LINUX_GLIBC_2_33 = '{}linux/gclib-2-33/libstable.so'.format(BASE)
PATH_MAC_OS_ARM = '{}macOS/arm/libstable.so'.format(BASE)
PATH_MAC_OS_I386 = '{}macOS/i386/libstable.so'.format(BASE)


def libstable_path(libstable_path=None) -> str:
    '''Get path to libstable.so'''
    if libstable_path is None:
        platform_id = platform.platform()

        if "Linux" in platform_id and "x86" in platform_id:

            if "2.31" in platform_id:
                # Linux-5.8.0-1039-azure-x86_64-with-glibc2.31
                # Linux-5.4.0-1045-aws-x86_64-with-glibc2.31
                libstable_path = PATH_LINUX_GLIBC_2_31

            elif "2.33" in platform_id:
                # Linux-5.12.14-arch1-1-x86_64-with-glibc2.33
                libstable_path = PATH_LINUX_GLIBC_2_33

        elif "macOS" in platform_id:

            if "arm" in platform_id:
                # macOS-11.4-arm64-arm-64bit
                libstable_path = PATH_MAC_OS_ARM

            elif "i386" in platform_id:
                # macOS-10.15.7-x86_64-i386-64bit
                libstable_path = PATH_MAC_OS_I386

        else:
            print('''OS not supported. Please use Linux w glibc 2.31 or 2.33,
                     macOS 11.4 arm64, or macOs 10.15.7 i386.''')

    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.abspath(os.path.join(path, os.pardir))
    return os.path.abspath(os.path.join(path, libstable_path))
